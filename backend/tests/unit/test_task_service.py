import pytest

from app.exceptions import ValidationError


def test_create_task_uses_defaults(task_service):
    task = task_service.create_task({"title": "Documentar entrega"})

    assert task["title"] == "Documentar entrega"
    assert task["description"] == ""
    assert task["priority"] == "medium"
    assert task["status"] == "todo"
    assert task["id"]


def test_create_task_rejects_short_title(task_service):
    with pytest.raises(ValidationError) as error:
        task_service.create_task({"title": "oi"})

    assert "pelo menos 3 caracteres" in str(error.value)


def test_update_task_status_changes_summary(task_service):
    task = task_service.create_task(
        {
            "title": "Subir conteineres",
            "priority": "high",
        }
    )

    updated = task_service.update_task_status(task["id"], {"status": "doing"})
    summary = task_service.get_summary()

    assert updated["status"] == "doing"
    assert summary["by_status"]["doing"] == 1
    assert summary["by_priority"]["high"] == 1


def test_delete_task_removes_it_from_repository(task_service):
    task = task_service.create_task({"title": "Remover item"})

    task_service.delete_task(task["id"])

    assert task_service.list_tasks() == []
