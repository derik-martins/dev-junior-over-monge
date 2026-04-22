import pytest

from app import create_app


@pytest.fixture
def app():
    app = create_app(
        {
            "TESTING": True,
            "SEED_DATA": False,
            "TASKS_REPOSITORY": "memory",
        }
    )
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def task_service(app):
    return app.extensions["task_service"]
