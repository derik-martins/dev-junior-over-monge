from __future__ import annotations

import time
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Dict, Protocol

from .models import Task

if TYPE_CHECKING:
    from psycopg import Connection


class TaskRepository(Protocol):
    def list(self) -> list[Task]:
        ...

    def get(self, task_id: str) -> Task | None:
        ...

    def add(self, task: Task) -> Task:
        ...

    def update(self, task: Task) -> Task:
        ...

    def delete(self, task_id: str) -> None:
        ...

    def clear(self) -> None:
        ...


class InMemoryTaskRepository:
    def __init__(self) -> None:
        self._tasks: Dict[str, Task] = {}

    def list(self) -> list[Task]:
        return sorted(
            self._tasks.values(),
            key=lambda task: task.created_at,
            reverse=True,
        )

    def get(self, task_id: str) -> Task | None:
        return self._tasks.get(task_id)

    def add(self, task: Task) -> Task:
        self._tasks[task.id] = task
        return task

    def update(self, task: Task) -> Task:
        self._tasks[task.id] = task
        return task

    def delete(self, task_id: str) -> None:
        self._tasks.pop(task_id, None)

    def clear(self) -> None:
        self._tasks.clear()


class PostgresTaskRepository:
    def __init__(
        self,
        dsn: str,
        connect_retries: int = 10,
        retry_delay: float = 1.0,
    ) -> None:
        self._dsn = dsn
        self._connect_retries = max(1, connect_retries)
        self._retry_delay = max(0.0, retry_delay)
        self._ensure_schema()

    def list(self) -> list[Task]:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, title, description, priority, status, created_at, updated_at
                    FROM tasks
                    ORDER BY created_at DESC
                    """
                )
                rows = cursor.fetchall()
        return [self._row_to_task(row) for row in rows]

    def get(self, task_id: str) -> Task | None:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, title, description, priority, status, created_at, updated_at
                    FROM tasks
                    WHERE id = %s
                    """,
                    (task_id,),
                )
                row = cursor.fetchone()
        if row is None:
            return None
        return self._row_to_task(row)

    def add(self, task: Task) -> Task:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO tasks (id, title, description, priority, status, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    self._task_params(task),
                )
        return task

    def update(self, task: Task) -> Task:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE tasks
                    SET title = %s,
                        description = %s,
                        priority = %s,
                        status = %s,
                        created_at = %s,
                        updated_at = %s
                    WHERE id = %s
                    """,
                    (
                        task.title,
                        task.description,
                        task.priority,
                        task.status,
                        self._parse_timestamp(task.created_at),
                        self._parse_timestamp(task.updated_at),
                        task.id,
                    ),
                )
        return task

    def delete(self, task_id: str) -> None:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))

    def clear(self) -> None:
        with self._connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute("TRUNCATE TABLE tasks")

    def _ensure_schema(self) -> None:
        last_error: Exception | None = None
        for attempt in range(1, self._connect_retries + 1):
            try:
                with self._connect() as connection:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            """
                            CREATE TABLE IF NOT EXISTS tasks (
                                id TEXT PRIMARY KEY,
                                title TEXT NOT NULL,
                                description TEXT NOT NULL,
                                priority TEXT NOT NULL,
                                status TEXT NOT NULL,
                                created_at TIMESTAMPTZ NOT NULL,
                                updated_at TIMESTAMPTZ NOT NULL
                            )
                            """
                        )
                return
            except Exception as error:
                last_error = error
                if attempt == self._connect_retries:
                    break
                time.sleep(self._retry_delay)
        raise RuntimeError("Nao foi possivel conectar ao PostgreSQL.") from last_error

    def _connect(self) -> Connection:
        psycopg = _load_psycopg()
        return psycopg.connect(self._dsn)

    @staticmethod
    def _row_to_task(row: tuple) -> Task:
        return Task(
            id=row[0],
            title=row[1],
            description=row[2],
            priority=row[3],
            status=row[4],
            created_at=PostgresTaskRepository._serialize_timestamp(row[5]),
            updated_at=PostgresTaskRepository._serialize_timestamp(row[6]),
        )

    @staticmethod
    def _task_params(task: Task) -> tuple[object, ...]:
        return (
            task.id,
            task.title,
            task.description,
            task.priority,
            task.status,
            PostgresTaskRepository._parse_timestamp(task.created_at),
            PostgresTaskRepository._parse_timestamp(task.updated_at),
        )

    @staticmethod
    def _parse_timestamp(value: str) -> datetime:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))

    @staticmethod
    def _serialize_timestamp(value: datetime) -> str:
        normalized = value.astimezone(timezone.utc).replace(microsecond=0)
        return normalized.isoformat().replace("+00:00", "Z")


def _load_psycopg():
    try:
        import psycopg
    except ImportError as error:
        raise RuntimeError(
            "A dependencia 'psycopg' nao esta instalada. Atualize o ambiente com as dependencias do backend."
        ) from error
    return psycopg
