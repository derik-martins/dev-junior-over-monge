from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from .exceptions import TaskNotFoundError, ValidationError
from .models import Task, VALID_PRIORITIES, VALID_STATUSES
from .repository import TaskRepository


class TaskService:
    def __init__(self, repository: TaskRepository) -> None:
        self.repository = repository

    def seed_defaults(self) -> None:
        if self.repository.list():
            return

        samples = (
            {
                "title": "Revisar briefing do teste",
                "description": "Validar o escopo, regras e critérios de entrega.",
                "priority": "high",
            },
            {
                "title": "Preparar ambiente Docker",
                "description": "Subir frontend e backend para validação do fluxo.",
                "priority": "medium",
            },
            {
                "title": "Registrar critérios de avaliação",
                "description": "Documentar o que será analisado na solução do candidato.",
                "priority": "low",
            },
        )

        for payload in samples:
            self.create_task(payload)

    def list_tasks(self) -> list[dict[str, str]]:
        return [task.to_dict() for task in self.repository.list()]

    def get_task(self, task_id: str) -> dict[str, str]:
        return self._get_task(task_id).to_dict()

    def create_task(self, payload: dict | None) -> dict[str, str]:
        data = payload or {}
        title = self._validate_title(data.get("title"))
        description = self._validate_description(data.get("description"))
        priority = self._validate_priority(data.get("priority", "medium"))
        timestamp = self._utc_now()
        task = Task(
            id=str(uuid4()),
            title=title,
            description=description,
            priority=priority,
            status="todo",
            created_at=timestamp,
            updated_at=timestamp,
        )
        return self.repository.add(task).to_dict()

    def update_task_status(self, task_id: str, payload: dict | None) -> dict[str, str]:
        data = payload or {}
        status = self._validate_status(data.get("status"))
        task = self._get_task(task_id)
        updated_task = task.with_updates(status=status, updated_at=self._utc_now())
        return self.repository.update(updated_task).to_dict()

    def delete_task(self, task_id: str) -> None:
        self._get_task(task_id)
        self.repository.delete(task_id)

    def get_summary(self) -> dict[str, object]:
        tasks = self.repository.list()
        by_status = {
            status: sum(1 for task in tasks if task.status == status)
            for status in VALID_STATUSES
        }
        by_priority = {
            priority: sum(1 for task in tasks if task.priority == priority)
            for priority in VALID_PRIORITIES
        }
        return {
            "total": len(tasks),
            "by_status": by_status,
            "by_priority": by_priority,
        }

    def _get_task(self, task_id: str) -> Task:
        task = self.repository.get(task_id)
        if task is None:
            raise TaskNotFoundError("Tarefa nao encontrada.")
        return task

    @staticmethod
    def _validate_title(value: object) -> str:
        if not isinstance(value, str):
            raise ValidationError("O campo title e obrigatorio.")
        normalized = value.strip()
        if len(normalized) < 3:
            raise ValidationError("O campo title precisa ter pelo menos 3 caracteres.")
        if len(normalized) > 120:
            raise ValidationError("O campo title pode ter no maximo 120 caracteres.")
        return normalized

    @staticmethod
    def _validate_description(value: object) -> str:
        if value is None:
            return ""
        if not isinstance(value, str):
            raise ValidationError("O campo description precisa ser texto.")
        normalized = value.strip()
        if len(normalized) > 500:
            raise ValidationError("O campo description pode ter no maximo 500 caracteres.")
        return normalized

    @staticmethod
    def _validate_priority(value: object) -> str:
        if not isinstance(value, str):
            raise ValidationError("O campo priority precisa ser texto.")
        normalized = value.strip().lower()
        if normalized not in VALID_PRIORITIES:
            raise ValidationError(
                f"Priority invalida. Use um destes valores: {', '.join(VALID_PRIORITIES)}."
            )
        return normalized

    @staticmethod
    def _validate_status(value: object) -> str:
        if not isinstance(value, str):
            raise ValidationError("O campo status e obrigatorio.")
        normalized = value.strip().lower()
        if normalized not in VALID_STATUSES:
            raise ValidationError(
                f"Status invalido. Use um destes valores: {', '.join(VALID_STATUSES)}."
            )
        return normalized

    @staticmethod
    def _utc_now() -> str:
        return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
