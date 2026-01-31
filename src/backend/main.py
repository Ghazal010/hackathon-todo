from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from sqlmodel import Session, select
from datetime import datetime
import json

from database import get_session, create_tables
from models import Task, TaskCreate, TaskUpdate, TaskResponse

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

# Helper function to convert SQLAlchemy model to response model
def task_to_response(task: Task) -> TaskResponse:
    # Parse tags from JSON string to list
    try:
        tags_list = json.loads(task.tags) if task.tags else []
    except json.JSONDecodeError:
        tags_list = []

    return TaskResponse(
        id=task.id,
        title=task.title,
        completed=task.completed,
        priority=task.priority,
        tags=tags_list,
        due_date=task.due_date,
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
    session: Session = Depends(get_session)
):
    """Get all tasks with optional filtering and search"""
    statement = select(Task)

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
async def create_task(task_data: TaskCreate, session: Session = Depends(get_session)):
    """Create a new task"""
    # Validate priority
    if task_data.priority not in ["high", "medium", "low"]:
        raise HTTPException(status_code=400, detail="Priority must be high, medium, or low")

    # Convert tags list to JSON string
    tags_json = json.dumps(task_data.tags) if task_data.tags else "[]"

    # Create new task
    new_task = Task(
        title=task_data.title,
        completed=task_data.completed,
        priority=task_data.priority,
        tags=tags_json,
        due_date=task_data.due_date
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
async def get_task(task_id: int, session: Session = Depends(get_session)):
    """Get a specific task by ID"""
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return {
        "success": True,
        "data": task_to_response(task)
    }

@app.put("/api/tasks/{task_id}")
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    session: Session = Depends(get_session)
):
    """Update a specific task by ID"""
    task = session.get(Task, task_id)
    if not task:
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
async def delete_task(task_id: int, session: Session = Depends(get_session)):
    """Delete a specific task by ID"""
    task = session.get(Task, task_id)
    if not task:
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
    session: Session = Depends(get_session)
):
    """Toggle the completion status of a task"""
    task = session.get(Task, task_id)
    if not task:
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
async def get_task_stats(session: Session = Depends(get_session)):
    """Get task statistics"""
    all_tasks = session.exec(select(Task)).all()

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