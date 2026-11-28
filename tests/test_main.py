import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, get_db
from main import app
from models import User as UserModel


# Isolated in-memory SQLite test database
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


# -------------------------
# Reusable test helpers
# -------------------------

def register_user(
    client,
    email="test@example.com",
    password="SecurePass123!"
):
    return client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password
        }
    )


def login_user(
    client,
    email="test@example.com",
    password="SecurePass123!"
):
    response = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": password
        }
    )

    return response


def authenticated_headers(client, email="test@example.com"):
    response = login_user(client, email=email)

    assert response.status_code == 200

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


def create_sample_task(client, headers):
    return client.post(
        "/tasks",
        headers=headers,
        json={
            "title": "Test Task",
            "description": "Testing the FastAPI application",
            "completed": False
        }
    )


# -------------------------
# Home endpoint
# -------------------------

def test_home_endpoint(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "Running successfully"
    assert response.json()["version"] == "8.0.0"
    assert response.json()["authentication"] == "JWT enabled"


# -------------------------
# Registration tests
# -------------------------

def test_register_user(client):
    response = register_user(client)

    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"
    assert response.json()["is_active"] is True
    assert "password" not in response.json()
    assert "hashed_password" not in response.json()


def test_register_duplicate_email(client):
    first_response = register_user(client)
    second_response = register_user(client)

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert "already exists" in second_response.json()["detail"]


def test_register_invalid_email(client):
    response = register_user(
        client,
        email="not-an-email"
    )

    assert response.status_code == 422


def test_register_short_password(client):
    response = register_user(
        client,
        password="short"
    )

    assert response.status_code == 422


def test_password_is_hashed(client):
    password = "SecurePass123!"

    response = register_user(
        client,
        password=password
    )

    assert response.status_code == 201

    db = TestingSessionLocal()

    try:
        user = db.query(UserModel).filter(
            UserModel.email == "test@example.com"
        ).first()

        assert user is not None
        assert user.hashed_password != password
        assert user.hashed_password.startswith("$argon2")
    finally:
        db.close()


# -------------------------
# Login and authentication tests
# -------------------------

def test_login_user(client):
    register_user(client)

    response = login_user(client)

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_wrong_password(client):
    register_user(client)

    response = login_user(
        client,
        password="WrongPassword123!"
    )

    assert response.status_code == 401


def test_login_unknown_user(client):
    response = login_user(
        client,
        email="unknown@example.com"
    )

    assert response.status_code == 401


def test_current_user_endpoint(client):
    register_user(client)

    headers = authenticated_headers(client)

    response = client.get(
        "/auth/me",
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"


def test_tasks_require_authentication(client):
    response = client.get("/tasks")

    assert response.status_code == 401


# -------------------------
# Task CRUD tests
# -------------------------

def test_create_task(client):
    register_user(client)
    headers = authenticated_headers(client)

    response = create_sample_task(client, headers)

    assert response.status_code == 200
    assert response.json()["message"] == "Task created successfully"
    assert response.json()["task"]["title"] == "Test Task"


def test_get_all_tasks(client):
    register_user(client)
    headers = authenticated_headers(client)

    create_sample_task(client, headers)

    response = client.get(
        "/tasks",
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["total_tasks"] == 1
    assert len(response.json()["tasks"]) == 1


def test_get_task_by_id(client):
    register_user(client)
    headers = authenticated_headers(client)

    create_sample_task(client, headers)

    response = client.get(
        "/tasks/1",
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["title"] == "Test Task"


def test_update_task(client):
    register_user(client)
    headers = authenticated_headers(client)

    create_sample_task(client, headers)

    response = client.put(
        "/tasks/1",
        headers=headers,
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
    register_user(client)
    headers = authenticated_headers(client)

    create_sample_task(client, headers)

    response = client.delete(
        "/tasks/1",
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted successfully"


# -------------------------
# Missing task tests
# -------------------------

def test_get_missing_task(client):
    register_user(client)
    headers = authenticated_headers(client)

    response = client.get(
        "/tasks/999",
        headers=headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_update_missing_task(client):
    register_user(client)
    headers = authenticated_headers(client)

    response = client.put(
        "/tasks/999",
        headers=headers,
        json={
            "title": "Updated Task",
            "description": "Testing missing task update",
            "completed": False
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_delete_missing_task(client):
    register_user(client)
    headers = authenticated_headers(client)

    response = client.delete(
        "/tasks/999",
        headers=headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_invalid_task_title(client):
    register_user(client)
    headers = authenticated_headers(client)

    response = client.post(
        "/tasks",
        headers=headers,
        json={
            "title": "AB",
            "description": "Testing invalid title",
            "completed": False
        }
    )

    assert response.status_code == 422


# -------------------------
# Task ownership tests
# -------------------------

def test_users_only_see_their_own_tasks(client):
    register_user(
        client,
        email="user1@example.com"
    )

    headers_user1 = authenticated_headers(
        client,
        email="user1@example.com"
    )

    create_sample_task(client, headers_user1)

    register_user(
        client,
        email="user2@example.com"
    )

    headers_user2 = authenticated_headers(
        client,
        email="user2@example.com"
    )

    response = client.get(
        "/tasks",
        headers=headers_user2
    )

    assert response.status_code == 200
    assert response.json()["total_tasks"] == 0
    assert response.json()["tasks"] == []


def test_user_cannot_view_another_users_task(client):
    register_user(
        client,
        email="user1@example.com"
    )

    headers_user1 = authenticated_headers(
        client,
        email="user1@example.com"
    )

    create_sample_task(client, headers_user1)

    register_user(
        client,
        email="user2@example.com"
    )

    headers_user2 = authenticated_headers(
        client,
        email="user2@example.com"
    )

    response = client.get(
        "/tasks/1",
        headers=headers_user2
    )

    assert response.status_code == 404


def test_user_cannot_update_another_users_task(client):
    register_user(
        client,
        email="user1@example.com"
    )

    headers_user1 = authenticated_headers(
        client,
        email="user1@example.com"
    )

    create_sample_task(client, headers_user1)

    register_user(
        client,
        email="user2@example.com"
    )

    headers_user2 = authenticated_headers(
        client,
        email="user2@example.com"
    )

    response = client.put(
        "/tasks/1",
        headers=headers_user2,
        json={
            "title": "Unauthorized Update",
            "description": "Trying to update another user's task",
            "completed": True
        }
    )

    assert response.status_code == 404


def test_user_cannot_delete_another_users_task(client):
    register_user(
        client,
        email="user1@example.com"
    )

    headers_user1 = authenticated_headers(
        client,
        email="user1@example.com"
    )

    create_sample_task(client, headers_user1)

    register_user(
        client,
        email="user2@example.com"
    )

    headers_user2 = authenticated_headers(
        client,
        email="user2@example.com"
    )

    response = client.delete(
        "/tasks/1",
        headers=headers_user2
    )

    assert response.status_code == 404
