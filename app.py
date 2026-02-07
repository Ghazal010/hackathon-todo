from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from datetime import datetime
import json
import os
from typing import List, Optional

# Import your existing models and database
from src.backend.database import get_session, create_tables
from src.backend.models import Task, TaskCreate, TaskUpdate, TaskResponse, User, UserRegister, UserLogin, UserResponse, Token
from src.backend.auth import authenticate_user, create_access_token, get_current_active_user, get_password_hash

# Import chat models and routes
from src.backend.chat_models import ChatRequest, ChatResponse
from src.backend.openai_client import chat_with_ai, execute_function, get_final_response

app = FastAPI(title="DreamFlow API", version="1.0.0")

# Add CORS middleware to allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables on startup
@app.on_event("startup")
def on_startup():
    create_tables()

@app.get("/")
def root():
    return {"message": "Welcome to DreamFlow API"}

# Include your existing routes here (copied from your main.py)
@app.get("/api/tasks")
async def get_tasks(
    filter_param: str = Query("all", alias="filter"),
    search: str = Query(""),
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """Get all tasks for the current user with optional filtering and search"""
    statement = select(Task)

    # Filter by current user's ID
    statement = statement.where(Task.user_id == current_user.id)

    # Apply search filter
    if search:
        statement = statement.where(Task.title.contains(search))

    # Apply status filter
    if filter_param == "active":
        statement = statement.where(Task.completed == False)
    elif filter_param == "completed":
        statement = statement.where(Task.completed == True)

    tasks = session.exec(statement).all()

    # Convert to response format
    task_responses = [task_to_response(task) for task in tasks]

    return {
        "success": True,
        "data": {
            "tasks": task_responses,
            "total": len(task_responses),
            "page": 1,
            "limit": len(task_responses)
        }
    }

@app.post("/api/tasks")
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """Create a new task for the current user"""
    # Validate priority
    if task_data.priority not in ["high", "medium", "low"]:
        raise HTTPException(status_code=400, detail="Priority must be high, medium, or low")

    # Convert tags list to JSON string
    tags_json = json.dumps(task_data.tags) if task_data.tags else "[]"

    # Create new task with current user's ID
    new_task = Task(
        title=task_data.title,
        completed=task_data.completed,
        priority=task_data.priority,
        tags=tags_json,
        due_date=task_data.due_date,
        user_id=current_user.id  # Set to current user's ID
    )

    session.add(new_task)
    session.commit()
    session.refresh(new_task)

    return {
        "success": True,
        "data": task_to_response(new_task),
        "message": "Task created successfully"
    }

# Add other routes as needed...

# Helper function to convert SQLAlchemy model to response model
def task_to_response(task: Task) -> TaskResponse:
    # Parse tags from JSON string to list
    try:
        tags_list = json.loads(task.tags) if task.tags else []
    except (json.JSONDecodeError, TypeError):
        tags_list = []

    return TaskResponse(
        id=task.id,
        title=task.title,
        completed=task.completed,
        priority=task.priority,
        tags=tags_list,
        due_date=task.due_date,
        user_id=task.user_id,
        created_at=task.created_at,
        updated_at=task.updated_at
    )

# Add all your other routes here...
# (registration, login, task management, chat routes, etc.)