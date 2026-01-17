#!/usr/bin/env python3
"""Test script for the Complete Task feature."""

import sys
import os
# Add the project root to the Python path to allow imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.task_manager import add_task, list_tasks, toggle_task_complete, TASKS
from src.utils import id_generator


def test_mark_incomplete_task_as_complete():
    """Test 1: Mark Incomplete Task as Complete"""
    print("Test 1: Mark Incomplete Task as Complete")

    # Clear any existing tasks
    TASKS.clear()
    id_generator._current_id = 0

    # Add task: "Buy groceries" (ID: 1, completed: False)
    task = add_task("Buy groceries")
    assert task["id"] == 1
    assert task["completed"] is False

    # Toggle task 1
    updated_task = toggle_task_complete(1)

    # Verify: Task 1 completed: True
    assert updated_task["completed"] is True
    print("✅ Mark incomplete task as complete test passed")


def test_mark_complete_task_as_incomplete():
    """Test 2: Mark Complete Task as Incomplete"""
    print("Test 2: Mark Complete Task as Incomplete")

    # Clear any existing tasks
    TASKS.clear()
    id_generator._current_id = 0

    # Add task and mark it complete
    task = add_task("Call mom")
    assert task["id"] == 1
    assert task["completed"] is False

    # Mark it complete first
    completed_task = toggle_task_complete(1)
    assert completed_task["completed"] is True

    # Now mark it incomplete
    incomplete_task = toggle_task_complete(1)
    assert incomplete_task["completed"] is False
    print("✅ Mark complete task as incomplete test passed")


def test_multiple_toggles():
    """Test 3: Multiple Toggles"""
    print("Test 3: Multiple Toggles")

    # Clear any existing tasks
    TASKS.clear()
    id_generator._current_id = 0

    # Add task: Task 1 incomplete
    task = add_task("Finish report")
    assert task["completed"] is False

    # Toggle 5 times
    # After 1st toggle: complete (True)
    task = toggle_task_complete(1)
    assert task["completed"] is True

    # After 2nd toggle: incomplete (False)
    task = toggle_task_complete(1)
    assert task["completed"] is False

    # After 3rd toggle: complete (True)
    task = toggle_task_complete(1)
    assert task["completed"] is True

    # After 4th toggle: incomplete (False)
    task = toggle_task_complete(1)
    assert task["completed"] is False

    # After 5th toggle: complete (True)
    task = toggle_task_complete(1)
    assert task["completed"] is True

    print("✅ Multiple toggles test passed")


def test_invalid_task_id():
    """Test 4: Invalid Task ID"""
    print("Test 4: Invalid Task ID")

    # Clear any existing tasks
    TASKS.clear()
    id_generator._current_id = 0

    # Add tasks with IDs 1, 2, 3
    add_task("Task 1")
    add_task("Task 2")
    add_task("Task 3")

    # Try to toggle task ID 999
    try:
        toggle_task_complete(999)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Task with ID 999 not found" in str(e)
        print("✅ Invalid task ID test passed")


def test_error_message_format():
    """Test that error messages are properly formatted"""
    print("Test: Error Message Format")

    # Clear any existing tasks
    TASKS.clear()
    id_generator._current_id = 0

    # Try to toggle non-existent task
    try:
        toggle_task_complete(1)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert str(e) == "Task with ID 1 not found"
        print("✅ Error message format test passed")


def test_toggle_after_deletion_logic():
    """Test 5: Toggle After Deletion Logic (Note: We don't have delete yet, but testing the concept)"""
    print("Test 5: Toggle functionality verification")

    # Clear any existing tasks
    TASKS.clear()
    id_generator._current_id = 0

    # Add tasks
    task1 = add_task("Task One")
    task2 = add_task("Task Two")
    task3 = add_task("Task Three")

    # Verify all tasks exist
    tasks = list_tasks()
    assert len(tasks) == 3

    # Toggle task 2 to complete
    updated_task2 = toggle_task_complete(2)
    assert updated_task2["completed"] is True

    # Verify other tasks are unaffected
    all_tasks = list_tasks()
    task1_found = next((t for t in all_tasks if t["id"] == 1), None)
    task3_found = next((t for t in all_tasks if t["id"] == 3), None)
    task2_found = next((t for t in all_tasks if t["id"] == 2), None)

    assert task1_found["completed"] is False
    assert task3_found["completed"] is False
    assert task2_found["completed"] is True

    print("✅ Toggle functionality verification passed")


def run_all_tests():
    """Run all test cases for Complete Task feature."""
    print("Running Complete Task feature tests...\n")

    test_mark_incomplete_task_as_complete()
    test_mark_complete_task_as_incomplete()
    test_multiple_toggles()
    test_invalid_task_id()
    test_error_message_format()
    test_toggle_after_deletion_logic()

    print("\n🎉 All Complete Task tests passed!")


if __name__ == "__main__":
    run_all_tests()