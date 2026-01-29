#!/usr/bin/env python3
"""Main CLI application for the Todo application."""

import sys
import os
from typing import Dict, List

# Add the project root to the Python path to allow imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.task_manager import add_task, list_tasks, toggle_task_complete, update_task, delete_task
from src.utils import display_tasks
from src.ai_features import suggest_task_improvement


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
    print("6. AI Task Improvement")
    print("7. Exit")
    print("-"*40)


def get_user_choice() -> str:
    """Get user's menu choice."""
    return input("Choose option (1-6): ").strip()


def handle_add_task(tasks: List[Dict]) -> None:
    """Handle the add task functionality."""
    print()
    title = input("Enter task title: ")

    description = input("Enter description (optional): ")

    # Ask if user wants AI improvement suggestions
    print()
    ai_improve = input("Would you like AI to suggest improvements? (y/n): ").lower().strip()

    if ai_improve == 'y':
        print("Getting AI suggestions...")
        try:
            suggestion = suggest_task_improvement(title, description)
            if suggestion:
                print("\nAI Suggestions:")
                if suggestion.get("title_suggestion"):
                    print(f"  Title: {suggestion['title_suggestion']}")
                if suggestion.get("description_suggestion"):
                    print(f"  Description: {suggestion['description_suggestion']}")

                accept = input("\nAccept suggestions? (y/n): ").lower().strip()
                if accept == 'y':
                    title = suggestion.get("title_suggestion", title)
                    description = suggestion.get("description_suggestion", description)
                    print("Suggestions applied!")
                else:
                    print("Original task kept as is.")
            else:
                print("Could not get AI suggestions. Using original task.")
        except Exception as e:
            print(f"AI suggestion failed: {str(e)}. Using original task.")

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


def handle_ai_task_improvement(tasks: List[Dict]) -> None:
    """Handle AI task improvement functionality."""
    print()

    # Get all tasks to choose from
    all_tasks = list_tasks()
    if not all_tasks:
        print("❌ No tasks available to improve. Add some tasks first.")
        print("\nPress Enter to continue...")
        input()
        return

    print("Select a task to get AI improvement suggestions:")
    for task in all_tasks:
        status_icon = "✅" if task["completed"] else "⬜"
        print(f"  [{task['id']}] {status_icon} {task['title']}")

    task_id_input = input("\nEnter task ID: ").strip()

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

    # Find the task
    selected_task = None
    for task in all_tasks:
        if task["id"] == task_id:
            selected_task = task
            break

    if selected_task is None:
        print(f"\n❌ Error: Task with ID {task_id} not found")
        print("\nPress Enter to continue...")
        input()
        return

    print(f"\nImproving task: [{selected_task['id']}] {selected_task['title']}")
    print("Getting AI suggestions...")

    try:
        suggestion = suggest_task_improvement(selected_task['title'], selected_task['description'])
        if suggestion:
            print("\nAI Suggestions:")
            if suggestion.get("title_suggestion"):
                print(f"  Title: {suggestion['title_suggestion']}")
            else:
                print(f"  Title: [Keep current - already good]")

            if suggestion.get("description_suggestion"):
                print(f"  Description: {suggestion['description_suggestion']}")
            else:
                print(f"  Description: [Keep current - already good]")

            print(f"  Priority: {suggestion.get('priority_level', 'Not specified')}")
            print(f"  Estimated time: {suggestion.get('estimated_time', 'Not specified')}")

            # Ask if user wants to apply suggestions
            apply_suggestions = input("\nApply these suggestions? (y/n): ").lower().strip()
            if apply_suggestions == 'y':
                # Prepare updates
                title_update = suggestion.get("title_suggestion")
                desc_update = suggestion.get("description_suggestion")

                # Only update if suggestions exist
                if title_update and title_update != selected_task['title']:
                    title_update = title_update
                else:
                    title_update = None

                if desc_update and desc_update != selected_task['description']:
                    desc_update = desc_update
                else:
                    desc_update = None

                if title_update is not None or desc_update is not None:
                    updated_task = update_task(task_id, title_update, desc_update)
                    print(f"\n✅ Task updated with AI suggestions!")
                    status_icon = "✅" if updated_task["completed"] else "⬜"
                    print(f"   [{updated_task['id']}] {status_icon} {updated_task['title']}")
                    if updated_task.get('description'):
                        print(f"       Description: {updated_task['description']}")
                else:
                    print("\n✅ No changes needed - task is already well-structured!")
            else:
                print("\n❌ Suggestions not applied.")
        else:
            print("\n❌ Could not get AI suggestions for this task.")
    except Exception as e:
        print(f"\n❌ AI improvement failed: {str(e)}")

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
            handle_ai_task_improvement([])  # Handle AI task improvement
        elif choice == "7":
            print("\nGoodbye! 👋")
            sys.exit(0)
        else:
            print("\nInvalid option. Please choose 1-7.")

        # Pause before showing menu again
        if choice in ["1", "2", "3", "4", "5", "6"]:
            print("\nPress Enter to continue...")
            input()


if __name__ == "__main__":
    main()