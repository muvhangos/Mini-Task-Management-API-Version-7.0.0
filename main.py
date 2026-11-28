from datetime import datetime, timedelta, timezone
import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

# Load environment variables before initializing the database.
load_dotenv()

from database import engine, Base, get_db
from models import Task as TaskModel, User as UserModel

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError(
        "SECRET_KEY is missing. Configure it in your .env file "
        "or deployment environment."
    )

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Create database tables if they do not already exist.
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Mini Task Management API",
    description=(
        "A secure task management API built with Python, FastAPI, "
        "SQLAlchemy, SQLite/PostgreSQL, Argon2 and JWT authentication."
    ),
    version="8.0.0"
)


# -------------------------
# Request and response models
# -------------------------

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class TaskCreate(BaseModel):
    title: str = Field(
        min_length=3,
        max_length=100,
        description="Task title must contain 3 to 100 characters"
    )
    description: str = Field(
        min_length=5,
        max_length=500,
        description="Task description must contain 5 to 500 characters"
    )
    completed: bool = False


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    completed: bool

    model_config = ConfigDict(from_attributes=True)


class TaskListResponse(BaseModel):
    total_tasks: int
    tasks: list[TaskResponse]


class TaskMessageResponse(BaseModel):
    message: str
    task: TaskResponse


# -------------------------
# Authentication functions
# -------------------------

def create_access_token(user_id: int) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "exp": expires_at
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate authentication credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        subject = payload.get("sub")

        if subject is None:
            raise credentials_exception

        user_id = int(subject)

    except (JWTError, ValueError, TypeError):
        raise credentials_exception

    user = db.query(UserModel).filter(
        UserModel.id == user_id
    ).first()

    if user is None:
        raise credentials_exception

    if not user.is_active or user.is_legacy:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account is not permitted to access the API"
        )

    return user


def get_user_task(
    task_id: int,
    user_id: int,
    db: Session
):
    task = db.query(TaskModel).filter(
        TaskModel.id == task_id,
        TaskModel.user_id == user_id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


# -------------------------
# Home endpoint
# -------------------------

@app.get("/")
def home():
    return {
        "message": "Welcome to Mini Task Management API!",
        "status": "Running successfully",
        "database": f"{engine.dialect.name} connected",
        "version": "8.0.0",
        "authentication": "JWT enabled"
    }


# -------------------------
# User registration
# -------------------------

@app.post(
    "/auth/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    normalized_email = str(user_data.email).strip().lower()

    existing_user = db.query(UserModel).filter(
        UserModel.email == normalized_email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists"
        )

    new_user = UserModel(
        email=normalized_email,
        hashed_password=password_hash.hash(user_data.password),
        is_active=True,
        is_legacy=False
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# -------------------------
# User login
# -------------------------

@app.post(
    "/auth/login",
    response_model=TokenResponse
)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    normalized_email = form_data.username.strip().lower()

    user = db.query(UserModel).filter(
        UserModel.email == normalized_email
    ).first()

    invalid_login = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Bearer"}
    )

    if user is None:
        raise invalid_login

    if not password_hash.verify(
        form_data.password,
        user.hashed_password
    ):
        raise invalid_login

    if not user.is_active or user.is_legacy:
        raise invalid_login

    access_token = create_access_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# -------------------------
# Current authenticated user
# -------------------------

@app.get(
    "/auth/me",
    response_model=UserResponse
)
def get_my_account(
    current_user: UserModel = Depends(get_current_user)
):
    return current_user


# -------------------------
# Create a task
# -------------------------

@app.post(
    "/tasks",
    response_model=TaskMessageResponse
)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    new_task = TaskModel(
        title=task.title,
        description=task.description,
        completed=task.completed,
        user_id=current_user.id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {
        "message": "Task created successfully",
        "task": new_task
    }


# -------------------------
# Get all tasks for current user
# -------------------------

@app.get(
    "/tasks",
    response_model=TaskListResponse
)
def get_tasks(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    tasks = db.query(TaskModel).filter(
        TaskModel.user_id == current_user.id
    ).order_by(TaskModel.id).all()

    return {
        "total_tasks": len(tasks),
        "tasks": tasks
    }


# -------------------------
# Get one task
# -------------------------

@app.get(
    "/tasks/{task_id}",
    response_model=TaskResponse
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return get_user_task(
        task_id,
        current_user.id,
        db
    )


# -------------------------
# Update a task
# -------------------------

@app.put(
    "/tasks/{task_id}",
    response_model=TaskMessageResponse
)
def update_task(
    task_id: int,
    updated_task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    task = get_user_task(
        task_id,
        current_user.id,
        db
    )

    task.title = updated_task.title
    task.description = updated_task.description
    task.completed = updated_task.completed

    db.commit()
    db.refresh(task)

    return {
        "message": "Task updated successfully",
        "task": task
    }


# -------------------------
# Delete a task
# -------------------------

@app.delete(
    "/tasks/{task_id}",
    response_model=TaskMessageResponse
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    task = get_user_task(
        task_id,
        current_user.id,
        db
    )

    deleted_task = {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed
    }

    db.delete(task)
    db.commit()

    return {
        "message": "Task deleted successfully",
        "task": deleted_task
    }
