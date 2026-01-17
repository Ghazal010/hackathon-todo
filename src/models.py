"""Models for the Todo application."""

from typing import TypedDict
from datetime import datetime


class Task(TypedDict):
    """
    Represents a task in the todo list.

    Attributes:
        id: Unique identifier for the task
        title: Task title (required, 1-200 characters)
        description: Task description (optional, max 1000 characters)
        completed: Whether the task is completed (default: False)
        created_at: ISO format timestamp when task was created
    """
    id: int
    title: str
    description: str
    completed: bool
    created_at: str