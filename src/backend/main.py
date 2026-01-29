from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import sqlite3
import json
from datetime import datetime
from contextlib import contextmanager

app = FastAPI(title="DreamFlow API", version="1.0.0")

# Add CORS middleware to allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for tasks (using SQLite would be better for persistence)
# But for simplicity in this implementation, we'll use a list
tasks_db = [
    {"id": 1, "title": "Design new landing page", "completed": False, "priority": "high", "tags": ["work"], "dueDate": "2024-02-15", "createdAt": "2024-01-29T10:30:00Z", "updatedAt": "2024-01-29T10:30:00Z"},
    {"id": 2, "title": "Morning meditation", "completed": True, "priority": "medium", "tags": ["personal"], "dueDate": "2024-02-10", "createdAt": "2024-01-29T10:30:00Z", "updatedAt": "2024-01-29T10:30:00Z"},
    {"id": 3, "title": "Grocery shopping", "completed": False, "priority": "low", "tags": ["errands"], "dueDate": "2024-02-12", "createdAt": "2024-01-29T10:30:00Z", "updatedAt": "2024-01-29T10:30:00Z"}
]

next_id = 4

def get_next_id():
    global next_id
    current_id = next_id
    next_id += 1
    return current_id

@app.get("/")
async def root():
    return {"message": "Welcome to DreamFlow API"}

@app.get("/api/tasks")
async def get_tasks(
    filter_param: str = Query("all", alias="filter"),
    search: str = Query("")
):
    """Get all tasks with optional filtering and search"""
    filtered_tasks = tasks_db

    # Apply search filter
    if search:
        filtered_tasks = [
            task for task in filtered_tasks
            if search.lower() in task["title"].lower()
        ]

    # Apply status filter
    if filter_param == "active":
        filtered_tasks = [task for task in filtered_tasks if not task["completed"]]
    elif filter_param == "completed":
        filtered_tasks = [task for task in filtered_tasks if task["completed"]]

    return {
        "success": True,
        "data": {
            "tasks": filtered_tasks,
            "total": len(filtered_tasks),
            "page": 1,
            "limit": len(filtered_tasks)
        }
    }

@app.post("/api/tasks")
async def create_task(task_data: dict):
    """Create a new task"""
    global next_id

    # Validate required fields
    if not task_data.get("title"):
        raise HTTPException(status_code=400, detail="Title is required")

    title = task_data["title"]
    priority = task_data.get("priority", "medium")
    tags = task_data.get("tags", [])
    due_date = task_data.get("dueDate", datetime.now().strftime("%Y-%m-%d"))

    # Validate priority
    if priority not in ["high", "medium", "low"]:
        raise HTTPException(status_code=400, detail="Priority must be high, medium, or low")

    # Create new task
    new_task = {
        "id": get_next_id(),
        "title": title,
        "completed": False,
        "priority": priority,
        "tags": tags,
        "dueDate": due_date,
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat()
    }

    tasks_db.append(new_task)

    return {
        "success": True,
        "data": new_task,
        "message": "Task created successfully"
    }

@app.get("/api/tasks/{task_id}")
async def get_task(task_id: int):
    """Get a specific task by ID"""
    task = next((t for t in tasks_db if t["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return {
        "success": True,
        "data": task
    }

@app.put("/api/tasks/{task_id}")
async def update_task(task_id: int, task_data: dict):
    """Update a specific task by ID"""
    task_index = next((i for i, t in enumerate(tasks_db) if t["id"] == task_id), None)
    if task_index is None:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update task fields
    updated_task = tasks_db[task_index].copy()

    if "title" in task_data:
        updated_task["title"] = task_data["title"]
    if "priority" in task_data:
        if task_data["priority"] in ["high", "medium", "low"]:
            updated_task["priority"] = task_data["priority"]
    if "tags" in task_data:
        updated_task["tags"] = task_data["tags"]
    if "dueDate" in task_data:
        updated_task["dueDate"] = task_data["dueDate"]
    if "completed" in task_data:
        updated_task["completed"] = task_data["completed"]

    updated_task["updatedAt"] = datetime.now().isoformat()

    tasks_db[task_index] = updated_task

    return {
        "success": True,
        "data": updated_task,
        "message": "Task updated successfully"
    }

@app.delete("/api/tasks/{task_id}")
async def delete_task(task_id: int):
    """Delete a specific task by ID"""
    global tasks_db

    task = next((t for t in tasks_db if t["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    tasks_db = [t for t in tasks_db if t["id"] != task_id]

    return {
        "success": True,
        "data": task,
        "message": "Task deleted successfully"
    }

@app.patch("/api/tasks/{task_id}/toggle-complete")
async def toggle_task_completion(task_id: int):
    """Toggle the completion status of a task"""
    task_index = next((i for i, t in enumerate(tasks_db) if t["id"] == task_id), None)
    if task_index is None:
        raise HTTPException(status_code=404, detail="Task not found")

    updated_task = tasks_db[task_index].copy()
    updated_task["completed"] = not updated_task["completed"]
    updated_task["updatedAt"] = datetime.now().isoformat()

    tasks_db[task_index] = updated_task

    return {
        "success": True,
        "data": updated_task,
        "message": "Task completion status updated"
    }

@app.get("/api/tasks/stats")
async def get_task_stats():
    """Get task statistics"""
    total = len(tasks_db)
    completed = len([t for t in tasks_db if t["completed"]])
    active = total - completed

    by_priority = {
        "high": len([t for t in tasks_db if t["priority"] == "high"]),
        "medium": len([t for t in tasks_db if t["priority"] == "medium"]),
        "low": len([t for t in tasks_db if t["priority"] == "low"])
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