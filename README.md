# Mini Task Management API

**Version 7.0.0**

A RESTful Task Management API built with Python and FastAPI. This project provides endpoints for creating, retrieving, updating, and deleting tasks, with persistent storage using SQLite.

## Features

- Create new tasks
- Retrieve all tasks
- Retrieve tasks by ID
- Update existing tasks
- Delete tasks
- SQLite database persistence
- SQLAlchemy database integration
- Pydantic data validation
- RESTful API endpoints
- Interactive Swagger documentation

## Technology Stack

- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- SQLite
- Pydantic

## Project Structure

```text
MiniFastAPI/
│
├── main.py
├── database.py
├── models.py
├── requirements.txt
├── README.md
├── .gitignore
└── tasks.db
```

## Installation

Clone the repository:

```bash
git clone https://github.com/muvhangos/Mini-Task-Management-API-Version-7.0.0.git
```

Navigate into the project:

```bash
cd Mini-Task-Management-API-Version-7.0.0
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

Start the development server:

```bash
python -m uvicorn main:app --reload
```

The API will run at:

http://127.0.0.1:8000

## API Documentation

FastAPI automatically generates interactive API documentation.

**Swagger UI:**

http://127.0.0.1:8000/docs

**ReDoc:**

http://127.0.0.1:8000/redoc

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Check API status |
| POST | `/tasks` | Create a new task |
| GET | `/tasks` | Retrieve all tasks |
| GET | `/tasks/{task_id}` | Retrieve a task by ID |
| PUT | `/tasks/{task_id}` | Update an existing task |
| DELETE | `/tasks/{task_id}` | Delete a task |

## Validation

Task data is validated using Pydantic.

- **Title:** 3–100 characters
- **Description:** 5–500 characters

Invalid requests return appropriate validation errors.

## Database

The project uses SQLite for data persistence and SQLAlchemy for database management.

The database is created and managed locally by the application.

## Developer

**Samuel Muvhango**

GitHub: [muvhangos](https://github.com/muvhangos)

---

*Mini Task Management API — Version 7.0.0*
