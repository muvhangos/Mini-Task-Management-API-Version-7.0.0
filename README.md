# Mini Task Management API

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)
![Pytest](https://img.shields.io/badge/Tests-Pytest-0A9EDC?logo=pytest&logoColor=white)
![CI](https://github.com/muvhangos/Mini-Task-Management-API-Version-7.0.0/actions/workflows/tests.yml/badge.svg)

**Version 7.0.0**

A RESTful backend application developed with Python, FastAPI, SQLAlchemy and SQLite. The project demonstrates API development, database integration, request validation, automated testing and Continuous Integration using GitHub Actions.

**Live API:** https://mini-task-management-api-version-7-0-0.onrender.com/

**Interactive Swagger Documentation:** https://mini-task-management-api-version-7-0-0.onrender.com/docs

**GitHub Repository:** https://github.com/muvhangos/Mini-Task-Management-API-Version-7.0.0

---

## Project Overview

The Mini Task Management API provides a structured REST API for managing tasks through standard HTTP methods.

It supports creating, retrieving, updating and deleting tasks, with SQLAlchemy handling database operations and Pydantic providing request and response validation.

The project also includes an automated pytest suite and a GitHub Actions CI workflow that runs tests on pushes and pull requests targeting the main branch.

## Key Features

- Create tasks using POST requests.
- Retrieve all tasks using GET requests.
- Retrieve individual tasks by ID.
- Update existing tasks using PUT requests.
- Delete tasks using DELETE requests.
- SQLite database integration.
- SQLAlchemy ORM.
- Pydantic request and response validation.
- Input validation and HTTP error handling.
- Interactive Swagger API documentation.
- Automated testing with pytest.
- Isolated in-memory SQLite test database.
- GitHub Actions Continuous Integration.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.14 | Backend programming |
| FastAPI | REST API framework |
| SQLAlchemy | Database ORM |
| SQLite | Database |
| Pydantic | Data validation and response schemas |
| Pytest | Automated testing |
| HTTPX2 | FastAPI test client integration |
| Git & GitHub | Version control |
| GitHub Actions | Continuous Integration |
| Render | API hosting |

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API health and welcome response |
| POST | `/tasks` | Create a task |
| GET | `/tasks` | Retrieve all tasks |
| GET | `/tasks/{task_id}` | Retrieve a task by ID |
| PUT | `/tasks/{task_id}` | Update a task |
| DELETE | `/tasks/{task_id}` | Delete a task |

### Example: Create a Task

**POST** `/tasks`

Request body:

```json
{
  "title": "Complete API development",
  "description": "Build and test a task management API",
  "completed": false
}
```

### Example: Successful Response

```json
{
  "message": "Task created successfully",
  "task": {
    "id": 1,
    "title": "Complete API development",
    "description": "Build and test a task management API",
    "completed": false
  }
}
```

### Validation and Error Handling

- Task title: 3–100 characters.
- Task description: 5–500 characters.
- Missing task: HTTP 404.
- Invalid request data: HTTP 422.

## Automated Testing

The project includes 10 automated tests covering:

- Home endpoint.
- Task creation.
- Retrieving all tasks.
- Retrieving a task by ID.
- Updating a task.
- Deleting a task.
- Retrieving a missing task.
- Updating a missing task.
- Deleting a missing task.
- Invalid task title validation.

**Latest verified local test result: 10 passed.**

Run the tests locally:

```powershell
python -m pytest -v
```

### GitHub Actions — Continuous Integration

The repository includes a GitHub Actions workflow:

`.github/workflows/tests.yml`

The workflow automatically runs when code is pushed to `main` or a pull request targets `main`.

It performs the following steps:

1. Checks out the repository.
2. Sets up Python 3.14.
3. Installs development dependencies.
4. Runs the automated pytest suite.

**First verified GitHub Actions run:** Successful.

[View GitHub Actions workflow](https://github.com/muvhangos/Mini-Task-Management-API-Version-7.0.0/actions)

## Run Locally

### 1. Clone the repository

```powershell
git clone https://github.com/muvhangos/Mini-Task-Management-API-Version-7.0.0.git
```

### 2. Enter the project directory

```powershell
cd Mini-Task-Management-API-Version-7.0.0
```

### 3. Create a virtual environment

```powershell
python -m venv venv
```

### 4. Activate the virtual environment

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install dependencies

For development and testing:

```powershell
python -m pip install -r requirements-dev.txt
```

### 6. Start the API

```powershell
uvicorn main:app --reload
```

### 7. Open the documentation

http://127.0.0.1:8000/docs

## Project Structure

```text
MiniFastAPI/
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── tests/
│   └── test_main.py
│
├── main.py
├── database.py
├── models.py
├── requirements.txt
├── requirements-dev.txt
├── pytest.ini
├── .gitignore
└── README.md
```

## Future Development — Version 8.0.0

Planned improvements:

- JWT authentication.
- User registration and login.
- Pagination and filtering.
- PostgreSQL database integration.
- Role-based access control.
- Expanded automated test coverage.

## Developer

**Samuel Muvhango**

Python Backend Developer | Full Stack Web Developer | IT & Systems Engineer

Johannesburg, South Africa

**Technical Focus:**
- Python
- FastAPI
- Flask and Django
- REST API development
- SQLAlchemy
- Automated testing
- GitHub Actions and CI
- Database integration
- AI-assisted development tools

**GitHub:** https://github.com/muvhangos

**LinkedIn:** https://www.linkedin.com/in/samuel-muvhango-78821a112

**Open to:** Junior Python Backend Developer, Junior API Developer and Python Engineer opportunities.

---

*This project demonstrates practical backend engineering skills through API development, database integration, automated testing and continuous integration.*