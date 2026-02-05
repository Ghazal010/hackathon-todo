from fastapi import FastAPI, HTTPException, Query, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from sqlmodel import Session, select
from datetime import datetime, timedelta
import json
from passlib.context import CryptContext

from .database import get_session, create_tables
from .models import (
    Task, TaskCreate, TaskUpdate, TaskResponse,
    User, UserRegister, UserLogin, UserResponse, Token
)
from .chat_routes import router as chat_router
from .auth import (
    authenticate_user, create_access_token,
    get_current_active_user, get_password_hash
)

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

# Register chat routes
app.include_router(chat_router)

# Authentication endpoints
@app.post("/api/register", response_model=UserResponse)
async def register_user(user_data: UserRegister, session: Session = Depends(get_session)):
    """Register a new user."""
    try:
        # Check if user already exists
        existing_user = session.query(User).filter(
            (User.email == user_data.email) | (User.username == user_data.username)
        ).first()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email or username already exists"
            )

        # Hash the password
        hashed_password = get_password_hash(user_data.password)

        # Create new user
        new_user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password
        )

        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        return new_user
    except HTTPException:
        raise
    except Exception as e:
        print(f"Registration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )

@app.post("/api/login", response_model=Token)
async def login_user(user_credentials: UserLogin, session: Session = Depends(get_session)):
    """Login a user and return access token."""
    user = authenticate_user(session, user_credentials.email, user_credentials.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/users/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Get current user's profile."""
    return current_user

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

@app.get("/")
async def root():
    return {"message": "Welcome to DreamFlow API"}

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

@app.get("/api/tasks/{task_id}")
async def get_task(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """Get a specific task by ID for the current user"""
    task = session.get(Task, task_id)
    if not task or task.user_id != current_user.id:  # Check if task belongs to current user
        raise HTTPException(status_code=404, detail="Task not found")

    return {
        "success": True,
        "data": task_to_response(task)
    }

@app.put("/api/tasks/{task_id}")
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """Update a specific task by ID for the current user"""
    task = session.get(Task, task_id)
    if not task or task.user_id != current_user.id:  # Check if task belongs to current user
        raise HTTPException(status_code=404, detail="Task not found")

    # Update task fields
    update_data = task_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        if field == "tags" and value is not None:
            # Convert tags list to JSON string
            setattr(task, field, json.dumps(value))
        else:
            setattr(task, field, value)

    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)

    return {
        "success": True,
        "data": task_to_response(task),
        "message": "Task updated successfully"
    }

@app.delete("/api/tasks/{task_id}")
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """Delete a specific task by ID for the current user"""
    task = session.get(Task, task_id)
    if not task or task.user_id != current_user.id:  # Check if task belongs to current user
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(task)
    session.commit()

    return {
        "success": True,
        "data": task_to_response(task),
        "message": "Task deleted successfully"
    }

@app.patch("/api/tasks/{task_id}/toggle-complete")
async def toggle_task_completion(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """Toggle the completion status of a task for the current user"""
    task = session.get(Task, task_id)
    if not task or task.user_id != current_user.id:  # Check if task belongs to current user
        raise HTTPException(status_code=404, detail="Task not found")

    task.completed = not task.completed
    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)

    return {
        "success": True,
        "data": task_to_response(task),
        "message": "Task completion status updated"
    }

@app.get("/api/tasks/stats")
async def get_task_stats(
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """Get task statistics for the current user"""
    # Filter by current user's ID
    all_tasks = session.exec(select(Task).where(Task.user_id == current_user.id)).all()

    total = len(all_tasks)
    completed = len([t for t in all_tasks if t.completed])
    active = total - completed

    by_priority = {
        "high": len([t for t in all_tasks if t.priority == "high"]),
        "medium": len([t for t in all_tasks if t.priority == "medium"]),
        "low": len([t for t in all_tasks if t.priority == "low"])
    }

    return {
        "success": True,
        "data": {
            "total": total,
            "completed": completed,
            "active": active,
            "byPriority": by_priority
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)