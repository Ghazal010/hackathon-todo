from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from sqlalchemy import JSON

class TaskBase(SQLModel):
    title: str
    completed: bool = False
    priority: str = "medium"  # "high", "medium", "low"
    tags: Optional[str] = "[]"  # Store as JSON string
    due_date: Optional[str] = None  # ISO date format

class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TaskCreate(TaskBase):
    pass  # Same as base but without ID

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    tags: Optional[str] = None
    due_date: Optional[str] = None

class TaskResponse(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime