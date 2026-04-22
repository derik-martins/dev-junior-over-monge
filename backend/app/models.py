from __future__ import annotations

from dataclasses import asdict, dataclass, replace

VALID_STATUSES = ("todo", "doing", "done")
VALID_PRIORITIES = ("low", "medium", "high")


@dataclass(frozen=True, slots=True)
class Task:
    id: str
    title: str
    description: str
    priority: str
    status: str
    created_at: str
    updated_at: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)

    def with_updates(self, **changes: str) -> "Task":
        return replace(self, **changes)
