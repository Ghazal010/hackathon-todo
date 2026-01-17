"""Task management functions for the Todo application."""

from typing import Dict, List, Optional
from datetime import datetime
from .models import Task
from .utils import generate_id, get_current_timestamp


# Global task storage (in-memory)
TASKS: List[Task] = []


def add_task(title: str, description: str = "") -> Dict:
    """
    Add a new task to the task list.

    Args:
        title: Task title (required, 1-200 characters)
        description: Task description (optional, max 1000 characters)

    Returns:
        dict: Created task with id, title, description, completed, created_at

    Raises:
        ValueError: If title is invalid or description too long
    """
    # Validate title
    if not title or not title.strip():
        raise ValueError("Title cannot be empty")

    stripped_title = title.strip()
    if len(stripped_title) > 200:
        raise ValueError("Title too long (max 200 characters)")

    # Validate description
    if len(description) > 1000:
        raise ValueError("Description too long (max 1000 characters)")

    # Create the task with validated inputs
    task: Task = {
        "id": generate_id(),
        "title": stripped_title,
        "description": description,
        "completed": False,
        "created_at": get_current_timestamp()
    }

    TASKS.append(task)

    return task


def list_tasks() -> List[Dict]:
    """
    Get all tasks from the task list.

    Returns:
        list[dict]: List of all tasks, or empty list if none exist
    """
    return [dict(task) for task in TASKS]  # Convert TypedDict to regular dict for compatibility


def toggle_task_complete(task_id: int) -> Dict:
    """
    Toggle the completion status of a task.

    Args:
        task_id: ID of the task to toggle

    Returns:
        dict: Updated task with new completion status

    Raises:
        ValueError: If task_id not found
    """
    # Find the task with the given ID
    for task in TASKS:
        if task["id"] == task_id:
            # Toggle the completion status
            task["completed"] = not task["completed"]
            return dict(task)  # Return the updated task

    # If we reach here, the task was not found
    raise ValueError(f"Task with ID {task_id} not found")


def update_task(task_id: int, title: str = None, description: str = None) -> Dict:
    """
    Update a task's title and/or description.

    Args:
        task_id: ID of the task to update
        title: New title (optional, must be valid if provided)
        description: New description (optional)

    Returns:
        dict: Updated task

    Raises:
        ValueError: If task_id not found or validation fails
    """
    # Find the task with the given ID
    task_to_update = None
    for task in TASKS:
        if task["id"] == task_id:
            task_to_update = task
            break

    if task_to_update is None:
        raise ValueError(f"Task with ID {task_id} not found")

    # Check if at least one field is provided for update
    if title is None and description is None:
        raise ValueError("No changes provided. Task remains unchanged.")

    # Prepare the updated task with current values
    updated_task = task_to_update.copy()

    # Update title if provided
    if title is not None:
        # Validate title
        if not title or not title.strip():
            raise ValueError("Title cannot be empty")

        stripped_title = title.strip()
        if len(stripped_title) > 200:
            raise ValueError("Title too long (max 200 characters)")

        updated_task["title"] = stripped_title

    # Update description if provided
    if description is not None:
        if len(description) > 1000:
            raise ValueError("Description too long (max 1000 characters)")

        updated_task["description"] = description

    # Update the task in the global list
    for i, task in enumerate(TASKS):
        if task["id"] == task_id:
            TASKS[i] = updated_task
            break

    return dict(updated_task)


def delete_task(task_id: int) -> Dict:
    """
    Delete a task from the task list.

    Args:
        task_id: ID of the task to delete

    Returns:
        dict: The deleted task (for confirmation message)

    Raises:
        ValueError: If task_id not found
    """
    # Find the task with the given ID
    task_to_delete = None
    task_index = -1

    for i, task in enumerate(TASKS):
        if task["id"] == task_id:
            task_to_delete = task
            task_index = i
            break

    if task_to_delete is None:
        raise ValueError(f"Task with ID {task_id} not found")

    # Remove the task from the list
    deleted_task = TASKS.pop(task_index)

    return dict(deleted_task)