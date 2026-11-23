
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from database import engine, Base, get_db
from models import Task as TaskModel


# Create database tables automatically
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Mini Task Management API",
    description="A task management API built with Python, FastAPI and SQLite",
    version="7.0.0"
)


# ==========================================
# PYDANTIC REQUEST MODELS
# ==========================================

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


# ==========================================
# PYDANTIC RESPONSE MODELS
# ==========================================

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


# ==========================================
# HOME ENDPOINT
# ==========================================

@app.get("/")
def home():
    return {
        "message": "Welcome to Mini Task Management API!",
        "status": "Running successfully",
        "database": "SQLite connected",
        "version": "7.0.0"
    }


# ==========================================
# CREATE TASK
# ==========================================

@app.post("/tasks", response_model=TaskMessageResponse)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
):

    new_task = TaskModel(
        title=task.title,
        description=task.description,
        completed=task.completed
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {
        "message": "Task created successfully",
        "task": new_task
    }


# ==========================================
# GET ALL TASKS
# ==========================================

@app.get("/tasks", response_model=TaskListResponse)
def get_tasks(db: Session = Depends(get_db)):

    tasks = db.query(TaskModel).order_by(TaskModel.id).all()

    return {
        "total_tasks": len(tasks),
        "tasks": tasks
    }


# ==========================================
# UPDATE TASK
# ==========================================

@app.put("/tasks/{task_id}", response_model=TaskMessageResponse)
def update_task(
    task_id: int,
    updated_task: TaskCreate,
    db: Session = Depends(get_db)
):

    task = db.query(TaskModel).filter(
        TaskModel.id == task_id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
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


# ==========================================
# DELETE TASK
# ==========================================

@app.delete("/tasks/{task_id}", response_model=TaskMessageResponse)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):

    task = db.query(TaskModel).filter(
        TaskModel.id == task_id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    deleted_task = task

    db.delete(task)
    db.commit()

    return {
        "message": "Task deleted successfully",
        "task": deleted_task
    }
