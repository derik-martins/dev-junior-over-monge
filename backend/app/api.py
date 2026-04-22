from __future__ import annotations

from flask import Blueprint, current_app, jsonify, request

api_bp = Blueprint("api", __name__, url_prefix="/api")


def _task_service():
    return current_app.extensions["task_service"]


@api_bp.get("/health")
def healthcheck():
    return jsonify(
        {
            "status": "ok",
            "service": "junior-challenge-api",
        }
    )


@api_bp.get("/tasks/summary")
def tasks_summary():
    return jsonify(_task_service().get_summary())


@api_bp.get("/tasks")
def list_tasks():
    return jsonify({"items": _task_service().list_tasks()})


@api_bp.get("/tasks/<task_id>")
def get_task(task_id: str):
    return jsonify(_task_service().get_task(task_id))


@api_bp.post("/tasks")
def create_task():
    payload = request.get_json(silent=True)
    task = _task_service().create_task(payload)
    return jsonify(task), 201


@api_bp.patch("/tasks/<task_id>/status")
def update_task_status(task_id: str):
    payload = request.get_json(silent=True)
    return jsonify(_task_service().update_task_status(task_id, payload))


@api_bp.delete("/tasks/<task_id>")
def delete_task(task_id: str):
    _task_service().delete_task(task_id)
    return jsonify({"message": "Tarefa removida com sucesso."}), 200
