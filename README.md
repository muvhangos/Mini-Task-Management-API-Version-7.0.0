# Mini Task Management API

![Python](https://img.shields.io/badge/Python-3.14-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.165.0-009688)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.1.9-red)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL%20%7C%20SQLite-blue)
![JWT](https://img.shields.io/badge/Auth-JWT-orange)
![Tests](https://img.shields.io/badge/Tests-Pytest-brightgreen)

**Version 8.0.0**

A secure RESTful task management API built with Python and FastAPI, featuring JWT authentication, password hashing, user-specific task management, and SQLite/PostgreSQL database support.

## Live Project

- **Live API:** https://mini-task-management-api-version-7-0-0.onrender.com/
- **Interactive API documentation:** https://mini-task-management-api-version-7-0-0.onrender.com/docs
- **GitHub repository:** https://github.com/muvhangos/Mini-Task-Management-API-Version-7.0.0

## Overview

Mini Task Management API is a backend development project demonstrating practical Python API engineering, authentication, database integration, data validation, automated testing, and deployment.

Version 8 introduces user registration, secure login, JWT-based authentication, and ownership-based access to tasks.

## Key Features

- RESTful API built with FastAPI.
- User registration and login.
- JWT access-token authentication.
- Argon2 password hashing.
- Protected task management endpoints.
- User-specific task ownership.
- SQLAlchemy ORM.
- SQLite for local development.
- PostgreSQL support for deployment.
- Pydantic request and response validation.
- Automated tests with Pytest.
- Interactive Swagger documentation.


## API Endpoints

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Authenticate and receive a JWT |
| GET | `/auth/me` | Retrieve the authenticated user |

### Task Management

| Method | Endpoint | Description |
|---|---|---|
| POST | `/tasks` | Create a task |
| GET | `/tasks` | List the user's tasks |
| GET | `/tasks/{task_id}` | Retrieve a specific task |
| PUT | `/tasks/{task_id}` | Update a task |
| DELETE | `/tasks/{task_id}` | Delete a task |

All task endpoints require a valid JWT access token. Users can only access their own tasks.

## Authentication Workflow

1. Register using `/auth/register`.
2. Log in using `/auth/login`.
3. Copy the returned access token.
4. Select **Authorize** in Swagger documentation.
5. Enter the bearer token.
6. Use the protected task endpoints.

The login endpoint accepts form data. Use the registered email address in the `username` field and your password in the `password` field.

## Validation and Security

- Email addresses are validated.
- Passwords must contain between 8 and 128 characters.
- Passwords are hashed using Argon2.
- JWT access tokens expire after 30 minutes.
- Duplicate email registration is rejected.
- Unauthenticated requests to protected endpoints are rejected.
- Task ownership is enforced through the authenticated user.

## Technology Stack

- Python 3.14
- FastAPI
- SQLAlchemy
- PostgreSQL and SQLite
- Pydantic
- JWT authentication
- Argon2 password hashing
- Pytest
- Uvicorn
- Render deployment
- GitHub Actions

## Run Locally

### 1. Clone the repository

git clone https://github.com/muvhangos/Mini-Task-Management-API-Version-7.0.0.git

### 2. Create a virtual environment

python -m venv venv

### 3. Activate the environment (Windows PowerShell)

.\venv\Scripts\Activate.ps1

### 4. Install dependencies

python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt

### 5. Configure environment variables

Create a .env file in the project root and add:

SECRET_KEY=replace-with-a-strong-random-secret

Never commit your .env file to GitHub.

### 6. Start the API

python -m uvicorn main:app --reload

Open the interactive API documentation:

http://127.0.0.1:8000/docs

SQLite is used by default. PostgreSQL can be configured through DATABASE_URL.

## Testing

Run the automated test suite:

python -m pytest -v

The project includes tests for API functionality, authentication, validation, and task management.

## Deployment

The application is configured for deployment on Render.

Deployment configuration:

- Build command: pip install -r requirements.txt
- Start command: uvicorn main:app --host 0.0.0.0 --port $PORT

Configure these environment variables in Render:

- SECRET_KEY
- DATABASE_URL

Use the PostgreSQL Internal Database URL for the web service when both services are in the same Render region.

## API Documentation

FastAPI automatically generates interactive Swagger documentation at:

/docs

The documentation allows developers to inspect endpoints, submit requests, and test authentication.

## Project Structure

- main.py — FastAPI application, authentication and API routes
- models.py — SQLAlchemy database models
- database.py — Database engine and session configuration
- tests/ — Automated API tests
- requirements.txt — Application dependencies
- requirements-dev.txt — Development and testing dependencies
- .github/workflows/ — GitHub Actions CI configuration

## Developer

**Samuel Muvhango**

Python Backend Developer | Full Stack Web Developer | IT & Systems Engineer

Johannesburg, South Africa

- GitHub: https://github.com/muvhangos
- LinkedIn: https://www.linkedin.com/in/samuel-muvhango-78821a112/

Open to Python Backend Engineer, FastAPI Developer and Full Stack Developer opportunities.

---

**Mini Task Management API — Version 8.0.0**

Built to demonstrate practical backend engineering, secure authentication, database integration, automated testing and cloud deployment.
