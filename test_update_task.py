#!/usr/bin/env python3
"""Test script for the Update Task feature."""

import sys
import os
# Add the project root to the Python path to allow imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.task_manager import add_task, update_task, TASKS
from src.utils import id_generator


def test_update_title_only():
    """Test 1: Update Title Only"""
    print("Test 1: Update Title Only")

    # Clear any existing tasks
    TASKS.clear()
    id_generator._current_id = 0

    # Setup: Task 1: "Buy groceries", description: "Milk"
    task = add_task("Buy groceries", "Milk")
    assert task["id"] == 1
    assert task["title"] == "Buy groceries"
    assert task["description"] == "Milk"

    # Action: Update title to: "Buy weekly groceries"
    updated_task = update_task(1, title="Buy weekly groceries")

    # Expected: Title changed to "Buy weekly groceries", description still "Milk"
    assert updated_task["title"] == "Buy weekly groceries"
    assert updated_task["description"] == "Milk"
    print("✅ Update title only test passed")


def test_update_description_only():
    """Test 2: Update Description Only"""
    print("Test 2: Update Description Only")

    # Clear any existing tasks
    TASKS.clear()
    id_generator._current_id = 0

    # Setup: Task 1: "Buy groceries", description: "Milk"
    task = add_task("Buy groceries", "Milk")
    assert task["title"] == "Buy groceries"
    assert task["description"] == "Milk"

    # Action: Update description to: "Milk, eggs, bread"
    updated_task = update_task(1, description="Milk, eggs, bread")

    # Expected: Title still "Buy groceries", description changed to "Milk, eggs, bread"
    assert updated_task["title"] == "Buy groceries"
    assert updated_task["description"] == "Milk, eggs, bread"
    print("✅ Update description only test passed")


def test_update_both_fields():
    """Test 3: Update Both Fields"""
    print("Test 3: Update Both Fields")

    # Clear any existing tasks
    TASKS.clear()
    id_generator._current_id = 0

    # Setup: Task 1: "Buy groceries", description: "Milk"
    task = add_task("Buy groceries", "Milk")
    assert task["title"] == "Buy groceries"
    assert task["description"] == "Milk"

    # Action: Update title to: "Shopping", description to: "Weekly shopping list"
    updated_task = update_task(1, title="Shopping", description="Weekly shopping list")

    # Expected: Both fields updated
    assert updated_task["title"] == "Shopping"
    assert updated_task["description"] == "Weekly shopping list"
    print("✅ Update both fields test passed")


def test_update_to_empty_description():
    """Test 4: Update to Empty Description"""
    print("Test 4: Update to Empty Description")

    # Clear any existing tasks
    TASKS.clear()
    id_generator._current_id = 0

    # Setup: Task 1 has description: "Some text"
    task = add_task("Test task", "Some text")
    assert task["description"] == "Some text"

    # Action: Update description to: ""
    updated_task = update_task(1, description="")

    # Expected: Description cleared (becomes ""), title unchanged
    assert updated_task["description"] == ""
    assert updated_task["title"] == "Test task"
    print("✅ Update to empty description test passed")


def test_invalid_title_update():
    """Test 5: Invalid Title Update"""
    print("Test 5: Invalid Title Update")

    # Clear any existing tasks
    TASKS.clear()
    id_generator._current_id = 0

    # Setup: Task 1 exists
    task = add_task("Valid task")
    assert task["title"] == "Valid task"

    # Action: Try to update title to empty string
    try:
        update_task(1, title="")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Title cannot be empty" in str(e)
        print("✅ Invalid empty title test passed")

    # Action: Try to update title to 201+ chars
    try:
        long_title = "a" * 201  # 201 characters
        update_task(1, title=long_title)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Title too long (max 200 characters)" in str(e)
        print("✅ Invalid long title test passed")


def test_update_non_existent_task():
    """Test 6: Update Non-existent Task"""
    print("Test 6: Update Non-existent Task")

    # Clear any existing tasks
    TASKS.clear()
    id_generator._current_id = 0

    # Setup: Only tasks 1, 2, 3 exist
    add_task("Task 1")
    add_task("Task 2")
    add_task("Task 3")

    # Action: Try to update task 5
    try:
        update_task(5, title="New title")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Task with ID 5 not found" in str(e)
        print("✅ Update non-existent task test passed")


def test_no_changes_provided():
    """Test 7: No Changes Provided"""
    print("Test 7: No Changes Provided")

    # Clear any existing tasks
    TASKS.clear()
    id_generator._current_id = 0

    # Setup: Task 1 exists
    task = add_task("Original task")

    # Action: Call update_task with no changes (both params None)
    try:
        update_task(1, title=None, description=None)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "No changes provided. Task remains unchanged." in str(e)
        print("✅ No changes provided test passed")


def test_whitespace_only_title():
    """Test Edge Case: Whitespace-only Title"""
    print("Test Edge Case: Whitespace-only Title")

    # Clear any existing tasks
    TASKS.clear()
    id_generator._current_id = 0

    # Setup: Task exists
    task = add_task("Original task")

    # Action: Try to update with whitespace-only title
    try:
        update_task(1, title="   ")  # Whitespace only
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Title cannot be empty" in str(e)
        print("✅ Whitespace-only title test passed")


def test_very_long_valid_updates():
    """Test Edge Case: Very Long Valid Updates"""
    print("Test Edge Case: Very Long Valid Updates")

    # Clear any existing tasks
    TASKS.clear()
    id_generator._current_id = 0

    # Setup: Task exists
    task = add_task("Original task")

    # Action: Update with exactly 200 char title and 1000 char description
    long_title = "a" * 200  # Exactly 200 characters
    long_desc = "b" * 1000  # Exactly 1000 characters

    updated_task = update_task(1, title=long_title, description=long_desc)

    # Expected: Both updates should work
    assert updated_task["title"] == long_title
    assert updated_task["description"] == long_desc
    print("✅ Very long valid updates test passed")


def test_completion_status_remains_unchanged():
    """Test Edge Case: Task Completion Status Remains Unchanged"""
    print("Test Edge Case: Task Completion Status Remains Unchanged")

    # Clear any existing tasks
    TASKS.clear()
    id_generator._current_id = 0

    # Setup: Task exists and is completed
    task = add_task("Test task")
    from src.task_manager import toggle_task_complete
    completed_task = toggle_task_complete(1)
    assert completed_task["completed"] is True

    # Action: Update the task title
    updated_task = update_task(1, title="Updated test task")

    # Expected: Completion status should remain True
    assert updated_task["completed"] is True
    assert updated_task["title"] == "Updated test task"
    print("✅ Completion status remains unchanged test passed")


def run_all_tests():
    """Run all test cases for Update Task feature."""
    print("Running Update Task feature tests...\n")

    test_update_title_only()
    test_update_description_only()
    test_update_both_fields()
    test_update_to_empty_description()
    test_invalid_title_update()
    test_update_non_existent_task()
    test_no_changes_provided()
    test_whitespace_only_title()
    test_very_long_valid_updates()
    test_completion_status_remains_unchanged()

    print("\n🎉 All Update Task tests passed!")


if __name__ == "__main__":
    run_all_tests()