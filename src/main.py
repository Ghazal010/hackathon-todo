#!/usr/bin/env python3
"""Main CLI application for the Todo application."""

import sys
import os
from typing import Dict, List

# Add the project root to the Python path to allow imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.task_manager import add_task, list_tasks, toggle_task_complete, update_task, delete_task
from src.utils import display_tasks


def display_menu() -> None:
    """Display the main menu options."""
    print("\n" + "="*40)
    print("TODO APPLICATION")
    print("="*40)
    print("1. Add Task")
    print("2. View All Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Task Complete")
    print("6. Exit")
    print("-"*40)


def get_user_choice() -> str:
    """Get user's menu choice."""
    return input("Choose option (1-6): ").strip()


def handle_add_task(tasks: List[Dict]) -> None:
    """Handle the add task functionality."""
    print()
    title = input("Enter task title: ")

    description = input("Enter description (optional): ")

    try:
        task = add_task(title, description)  # This already adds to global TASKS
        print(f"\n✅ Task added successfully! (ID: {task['id']})")
    except ValueError as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nPress Enter to continue...")
        input()


def handle_view_tasks(tasks: List[Dict]) -> None:
    """Handle viewing all tasks."""
    # Get all tasks from the global storage in task_manager
    all_tasks = list_tasks()
    display_tasks(all_tasks)


def handle_delete_task(tasks: List[Dict]) -> None:
    """Handle deleting a task."""
    print()

    # Check if there are any tasks to delete
    all_tasks = list_tasks()
    if not all_tasks:
        print("❌ No tasks to delete. Your task list is empty.")
        print("\nPress Enter to continue...")
        input()
        return

    task_id_input = input("Enter task ID to delete: ").strip()

    # Validate that the input is a number
    try:
        task_id = int(task_id_input)
    except ValueError:
        print(f"\n❌ Error: Please enter a valid task ID (number)")
        print("\nPress Enter to continue...")
        input()
        return

    # Validate that the task ID is positive
    if task_id <= 0:
        print(f"\n❌ Error: Task ID must be a positive number")
        print("\nPress Enter to continue...")
        input()
        return

    # Find and display the task to be deleted
    task_to_delete = None
    for task in all_tasks:
        if task["id"] == task_id:
            task_to_delete = task
            break

    if task_to_delete is None:
        print(f"\n❌ Error: Task with ID {task_id} not found")
        print("\nPress Enter to continue...")
        input()
        return

    # Show task details before deletion
    status_icon = "✅" if task_to_delete["completed"] else "⬜"
    print(f"\nTask to delete:")
    print(f"[{task_to_delete['id']}] {status_icon} {task_to_delete['title']}")
    if task_to_delete['description']:
        print(f"    Description: {task_to_delete['description']}")

    # Ask for confirmation
    print()
    response = input("This action cannot be undone. Continue? (y/n): ").lower().strip()
    if response != 'y':
        print(f"\n❌ Deletion cancelled. Task not deleted.")
        print("\nPress Enter to continue...")
        input()
        return

    try:
        deleted_task = delete_task(task_id)
        print(f"\n✅ Task deleted successfully!")
        print(f"   Deleted: [{deleted_task['id']}] {status_icon} {deleted_task['title']}")
        if deleted_task['description']:
            print(f"            Description: {deleted_task['description']}")

    except ValueError as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nPress Enter to continue...")
        input()


def handle_update_task(tasks: List[Dict]) -> None:
    """Handle updating task title and/or description."""
    print()
    task_id_input = input("Enter task ID: ").strip()

    # Validate that the input is a number
    try:
        task_id = int(task_id_input)
    except ValueError:
        print(f"\n❌ Error: Please enter a valid task ID (number)")
        print("\nPress Enter to continue...")
        input()
        return

    # Validate that the task ID is positive
    if task_id <= 0:
        print(f"\n❌ Error: Task ID must be a positive number")
        print("\nPress Enter to continue...")
        input()
        return

    # Find and display the current task
    all_tasks = list_tasks()
    current_task = None
    for task in all_tasks:
        if task["id"] == task_id:
            current_task = task
            break

    if current_task is None:
        print(f"\n❌ Error: Task with ID {task_id} not found")
        print("\nPress Enter to continue...")
        input()
        return

    # Show current task details
    status_icon = "✅" if current_task["completed"] else "⬜"
    print(f"\nCurrent task:")
    print(f"[{current_task['id']}] {status_icon} {current_task['title']}")
    if current_task['description']:
        print(f"    Description: {current_task['description']}")

    print()
    new_title = input("Update title (press Enter to keep current): ").strip()
    new_description = input("Update description (press Enter to keep current): ")

    # Determine what to update
    title_to_update = new_title if new_title else None
    description_to_update = new_description if new_description != "" else None

    # If no changes were entered, keep original values
    if title_to_update is None and description_to_update is None:
        print(f"\n❌ Error: No changes provided. Task remains unchanged.")
        print("\nPress Enter to continue...")
        input()
        return

    try:
        updated_task = update_task(task_id, title_to_update, description_to_update)
        status_icon = "✅" if updated_task["completed"] else "⬜"

        print(f"\n✅ Task updated successfully!")
        print(f"   [{updated_task['id']}] {status_icon} {updated_task['title']}")
        if updated_task['description']:
            print(f"       Description: {updated_task['description']}")

    except ValueError as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nPress Enter to continue...")
        input()


def handle_toggle_task_completion(tasks: List[Dict]) -> None:
    """Handle toggling task completion status."""
    print()
    task_id_input = input("Enter task ID: ").strip()

    # Validate that the input is a number
    try:
        task_id = int(task_id_input)
    except ValueError:
        print(f"\n❌ Error: Please enter a valid task ID (number)")
        print("\nPress Enter to continue...")
        input()
        return

    # Validate that the task ID is positive
    if task_id <= 0:
        print(f"\n❌ Error: Task ID must be a positive number")
        print("\nPress Enter to continue...")
        input()
        return

    try:
        updated_task = toggle_task_complete(task_id)
        status_text = "complete" if updated_task["completed"] else "incomplete"
        status_icon = "✅" if updated_task["completed"] else "⬜"

        print(f"\n✅ Task marked as {status_text}!")
        print(f"   [{updated_task['id']}] {status_icon} {updated_task['title']}")

    except ValueError as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nPress Enter to continue...")
        input()


def main() -> None:
    """Main application loop."""
    # Using global task storage, so no need to maintain local tasks list

    while True:
        display_menu()
        choice = get_user_choice()

        if choice == "1":
            handle_add_task([])  # Passing empty list since add_task uses global storage
        elif choice == "2":
            handle_view_tasks([])  # Passing empty list since view_tasks uses global storage
        elif choice == "3":
            handle_update_task([])  # Passing empty list since update_task uses global storage
        elif choice == "4":
            handle_delete_task([])  # Passing empty list since delete_task uses global storage
        elif choice == "5":
            handle_toggle_task_completion([])  # Passing empty list since toggle_task_complete uses global storage
        elif choice == "6":
            print("\nGoodbye! 👋")
            sys.exit(0)
        else:
            print("\nInvalid option. Please choose 1-6.")

        # Pause before showing menu again
        if choice in ["1", "2", "3", "4", "5"]:
            print("\nPress Enter to continue...")
            input()


if __name__ == "__main__":
    main()