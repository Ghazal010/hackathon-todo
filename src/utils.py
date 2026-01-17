"""Utility functions for the Todo application."""

import time
from datetime import datetime


class IdGenerator:
    """Simple ID generator that increments with each call."""
    def __init__(self):
        self._current_id = 0

    def generate_id(self) -> int:
        """Generate a new unique ID."""
        self._current_id += 1
        return self._current_id


# Global ID generator instance
id_generator = IdGenerator()


def generate_id() -> int:
    """
    Generate a new unique ID.

    Returns:
        int: A unique ID that increments with each call
    """
    return id_generator.generate_id()


def get_current_timestamp() -> str:
    """
    Get current timestamp in ISO 8601 format.

    Returns:
        str: Current timestamp in ISO format (e.g., '2025-12-01T10:30:00')
    """
    return datetime.now().isoformat()


def display_tasks(tasks: list) -> None:
    """
    Display tasks in a formatted, readable way.

    Args:
        tasks: List of task dictionaries to display
    """
    print("\n=== All Tasks ===\n")

    if not tasks:
        print("No tasks found. Add your first task!")
        return

    # Count completed and pending tasks
    completed_count = sum(1 for task in tasks if task.get('completed', False))
    total_count = len(tasks)
    pending_count = total_count - completed_count

    # Display each task
    for task in tasks:
        status_icon = "✅" if task.get('completed', False) else "⬜"
        task_id = task.get('id', 'N/A')
        title = task.get('title', '')

        # Format timestamp - convert from ISO to readable format
        created_at_iso = task.get('created_at', '')
        created_at_readable = format_timestamp(created_at_iso)

        print(f"[{task_id}] {status_icon} {title}")
        print(f"    Created: {created_at_readable}")

        # Only show description if it exists and is not empty
        description = task.get('description', '')
        if description:
            print(f"    Description: {description}")

        print()  # Blank line after each task

    # Print summary
    task_word = "task" if total_count == 1 else "tasks"
    completed_word = "completed" if completed_count == 1 else "completed"
    pending_word = "pending" if pending_count == 1 else "pending"

    print(f"Total: {total_count} {task_word} ({completed_count} {completed_word}, {pending_count} {pending_word})")


def format_timestamp(iso_timestamp: str) -> str:
    """
    Convert ISO timestamp to a more readable format.

    Args:
        iso_timestamp: ISO format timestamp (e.g., '2025-12-01T10:30:00')

    Returns:
        str: Human-readable timestamp (e.g., '2025-12-01 10:30')
    """
    try:
        # Parse the ISO format timestamp
        dt = datetime.fromisoformat(iso_timestamp.replace('Z', '+00:00'))
        # Format as 'YYYY-MM-DD HH:MM'
        return dt.strftime('%Y-%m-%d %H:%M')
    except Exception:
        # Fallback to original if parsing fails
        return iso_timestamp