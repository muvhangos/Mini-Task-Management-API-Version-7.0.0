
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, get_db
from main import app


# Create an isolated in-memory SQLite test database
TEST_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)


@pytest.fixture
def client():
    # Create fresh tables for each test
    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)


def create_sample_task(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Test Task",
            "description": "Testing the FastAPI application",
            "completed": False
        }
    )
    return response


def test_home_endpoint(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "Running successfully"
    assert response.json()["version"] == "7.0.0"


def test_create_task(client):
    response = create_sample_task(client)

    assert response.status_code == 200
    assert response.json()["message"] == "Task created successfully"
    assert response.json()["task"]["title"] == "Test Task"


def test_get_all_tasks(client):
    create_sample_task(client)

    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json()["total_tasks"] == 1
    assert len(response.json()["tasks"]) == 1


def test_get_task_by_id(client):
    create_sample_task(client)

    response = client.get("/tasks/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["title"] == "Test Task"


def test_update_task(client):
    create_sample_task(client)

    response = client.put(
        "/tasks/1",
        json={
            "title": "Updated Test Task",
            "description": "Testing the task update endpoint",
            "completed": True
        }
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Task updated successfully"
    assert response.json()["task"]["title"] == "Updated Test Task"
    assert response.json()["task"]["completed"] is True


def test_delete_task(client):
    create_sample_task(client)

    response = client.delete("/tasks/1")

    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted successfully"


def test_get_missing_task(client):
    response = client.get("/tasks/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_update_missing_task(client):
    response = client.put(
        "/tasks/999",
        json={
            "title": "Updated Task",
            "description": "Testing missing task update",
            "completed": False
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_delete_missing_task(client):
    response = client.delete("/tasks/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_invalid_task_title(client):
    response = client.post(
        "/tasks",
        json={
            "title": "AB",
            "description": "Testing invalid title",
            "completed": False
        }
    )

    assert response.status_code == 422
