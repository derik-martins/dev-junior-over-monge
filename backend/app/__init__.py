from __future__ import annotations

import os

from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException

from .api import api_bp
from .exceptions import AppError
from .repository import InMemoryTaskRepository, PostgresTaskRepository, TaskRepository
from .service import TaskService


def create_app(config_overrides: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(
        TESTING=False,
        APP_NAME="Junior Challenge API",
        SEED_DATA=os.getenv("APP_SEED_DATA", "true").lower() == "true",
        TASKS_REPOSITORY=os.getenv(
            "TASKS_REPOSITORY",
            "postgres" if os.getenv("DATABASE_URL") else "memory",
        ),
        DATABASE_URL=os.getenv("DATABASE_URL"),
        DATABASE_CONNECT_RETRIES=int(os.getenv("DATABASE_CONNECT_RETRIES", "10")),
        DATABASE_RETRY_DELAY=float(os.getenv("DATABASE_RETRY_DELAY", "1")),
    )

    if config_overrides:
        app.config.update(config_overrides)

    repository = _build_repository(app)
    service = TaskService(repository)
    if app.config["SEED_DATA"]:
        service.seed_defaults()

    app.extensions["task_service"] = service
    app.register_blueprint(api_bp)
    _register_error_handlers(app)
    return app


def _register_error_handlers(app: Flask) -> None:
    @app.errorhandler(AppError)
    def handle_app_error(error: AppError):
        return jsonify({"error": error.message}), error.status_code

    @app.errorhandler(HTTPException)
    def handle_http_error(error: HTTPException):
        if request.path.startswith("/api/"):
            return jsonify({"error": error.description}), error.code
        return error

    @app.errorhandler(Exception)
    def handle_unexpected_error(error: Exception):
        if request.path.startswith("/api/"):
            return jsonify({"error": "Erro interno nao tratado."}), 500
        raise error


def _build_repository(app: Flask) -> TaskRepository:
    repository_name = str(app.config["TASKS_REPOSITORY"]).strip().lower()
    if repository_name == "memory":
        return InMemoryTaskRepository()

    if repository_name == "postgres":
        dsn = app.config.get("DATABASE_URL")
        if not dsn:
            raise RuntimeError(
                "DATABASE_URL precisa ser informado quando TASKS_REPOSITORY=postgres."
            )
        return PostgresTaskRepository(
            dsn=dsn,
            connect_retries=int(app.config["DATABASE_CONNECT_RETRIES"]),
            retry_delay=float(app.config["DATABASE_RETRY_DELAY"]),
        )

    raise RuntimeError(
        "TASKS_REPOSITORY invalido. Use 'memory' ou 'postgres'."
    )
