#!/usr/bin/env python3
"""Test script for the Delete Task feature."""

import sys
import os
# Add the project root to the Python path to allow imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.task_manager import add_task, delete_task, list_tasks, TASKS
from src.utils import id_generator


def test_delete_existing_task():
    """Test 1: Delete Existing Task"""
    print("Test 1: Delete Existing Task")

    # Clear any existing tasks
    TASKS.clear()
    id_generator._current_id = 0

    # Setup: Tasks: 1, 2, 3
    add_task("Task 1")
    add_task("Task 2", "Description for task 2")
    add_task("Task 3")

    initial_tasks = list_tasks()
    assert len(initial_tasks) == 3

    # Action: Delete task 2
    deleted_task = delete_task(2)

    # Expected: Task 2 removed from list, Tasks 1 and 3 still exist, IDs remain 1 and 3
    remaining_tasks = list_tasks()
    assert len(remaining_tasks) == 2

    task_ids = [task["id"] for task in remaining_tasks]
    assert 1 in task_ids
    assert 3 in task_ids
    assert 2 not in task_ids  # Task 2 should be gone

    # Verify the deleted task details
    assert deleted_task["id"] == 2
    assert deleted_task["title"] == "Task 2"
    assert deleted_task["description"] == "Description for task 2"

    print("✅ Delete existing task test passed")


def test_delete_first_task():
    """Test 2: Delete First Task"""
    print("Test 2: Delete First Task")

    # Clear any existing tasks
    TASKS.clear()
    id_generator._current_id = 0

    # Setup: Tasks: 1, 2, 3
    add_task("Task 1")
    add_task("Task 2")
    add_task("Task 3")

    # Action: Delete task 1
    deleted_task = delete_task(1)

    # Expected: Task 1 removed, Tasks 2 and 3 remain with IDs 2 and 3, no renumbering
    remaining_tasks = list_tasks()
    assert len(remaining_tasks) == 2

    task_ids = [task["id"] for task in remaining_tasks]
    assert 2 in task_ids
    assert 3 in task_ids
    assert 1 not in task_ids  # Task 1 should be gone

    # Verify the deleted task details
    assert deleted_task["id"] == 1
    assert deleted_task["title"] == "Task 1"

    print("✅ Delete first task test passed")


def test_delete_last_task():
    """Test 3: Delete Last Task"""
    print("Test 3: Delete Last Task")

    # Clear any existing tasks
    TASKS.clear()
    id_generator._current_id = 0

    # Setup: Tasks: 1, 2, 3
    add_task("Task 1")
    add_task("Task 2")
    add_task("Task 3")

    # Action: Delete task 3
    deleted_task = delete_task(3)

    # Expected: Task 3 removed, Tasks 1 and 2 remain unchanged
    remaining_tasks = list_tasks()
    assert len(remaining_tasks) == 2

    task_ids = [task["id"] for task in remaining_tasks]
    assert 1 in task_ids
    assert 2 in task_ids
    assert 3 not in task_ids  # Task 3 should be gone

    # Verify the deleted task details
    assert deleted_task["id"] == 3
    assert deleted_task["title"] == "Task 3"

    print("✅ Delete last task test passed")


def test_delete_only_task():
    """Test 4: Delete Only Task"""
    print("Test 4: Delete Only Task")

    # Clear any existing tasks
    TASKS.clear()
    id_generator._current_id = 0

    # Setup: Only task 1 exists
    add_task("Only task")

    # Action: Delete task 1
    deleted_task = delete_task(1)

    # Expected: Task list becomes empty
    remaining_tasks = list_tasks()
    assert len(remaining_tasks) == 0

    # Verify the deleted task details
    assert deleted_task["id"] == 1
    assert deleted_task["title"] == "Only task"

    print("✅ Delete only task test passed")


def test_delete_nonexistent_task():
    """Test 5: Delete Non-existent Task"""
    print("Test 5: Delete Non-existent Task")

    # Clear any existing tasks
    TASKS.clear()
    id_generator._current_id = 0

    # Setup: Tasks: 1, 2, 3
    add_task("Task 1")
    add_task("Task 2")
    add_task("Task 3")

    # Action: Try to delete task 5
    try:
        delete_task(5)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        # Expected: ValueError raised with message "Task with ID 5 not found"
        assert "Task with ID 5 not found" in str(e)

        # No tasks should be deleted
        remaining_tasks = list_tasks()
        assert len(remaining_tasks) == 3
        task_ids = [task["id"] for task in remaining_tasks]
        assert set(task_ids) == {1, 2, 3}

        print("✅ Delete non-existent task test passed")


def test_delete_already_deleted_task():
    """Test 6: Delete Already Deleted Task"""
    print("Test 6: Delete Already Deleted Task")

    # Clear any existing tasks
    TASKS.clear()
    id_generator._current_id = 0

    # Setup: Task 2 was deleted earlier
    add_task("Task 1")
    add_task("Task 2")
    add_task("Task 3")

    # Delete task 2 first
    delete_task(2)

    # Action: Try to delete task 2 again
    try:
        delete_task(2)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        # Expected: Error: "Task with ID 2 not found"
        assert "Task with ID 2 not found" in str(e)

        # Other tasks should remain unchanged
        remaining_tasks = list_tasks()
        assert len(remaining_tasks) == 2
        task_ids = [task["id"] for task in remaining_tasks]
        assert set(task_ids) == {1, 3}

        print("✅ Delete already deleted task test passed")


def test_multiple_sequential_deletes():
    """Test 7: Multiple Sequential Deletes"""
    print("Test 7: Multiple Sequential Deletes")

    # Clear any existing tasks
    TASKS.clear()
    id_generator._current_id = 0

    # Setup: Tasks: 1, 2, 3, 4, 5
    for i in range(1, 6):
        add_task(f"Task {i}")

    # Action: Delete 2, then delete 4, then delete 1
    deleted_task_2 = delete_task(2)
    deleted_task_4 = delete_task(4)
    deleted_task_1 = delete_task(1)

    # Expected: Remaining tasks: 3, 5 with IDs unchanged
    remaining_tasks = list_tasks()
    assert len(remaining_tasks) == 2

    task_ids = [task["id"] for task in remaining_tasks]
    assert set(task_ids) == {3, 5}  # Only tasks 3 and 5 should remain
    assert 1 not in task_ids and 2 not in task_ids and 4 not in task_ids

    # Verify each deletion showed correct confirmation
    assert deleted_task_2["id"] == 2
    assert deleted_task_4["id"] == 4
    assert deleted_task_1["id"] == 1

    print("✅ Multiple sequential deletes test passed")


def test_id_persistence_after_deletion():
    """Test Edge Case: IDs remain unchanged after deletion"""
    print("Test Edge Case: IDs remain unchanged after deletion")

    # Clear any existing tasks
    TASKS.clear()
    id_generator._current_id = 0

    # Add a few tasks
    task1 = add_task("First task")
    task2 = add_task("Second task")
    task3 = add_task("Third task")

    # Verify initial IDs
    assert task1["id"] == 1
    assert task2["id"] == 2
    assert task3["id"] == 3

    # Delete middle task
    delete_task(2)

    # Add a new task - it should get the next ID (4, not reusing 2)
    new_task = add_task("New task")
    assert new_task["id"] == 4

    # Verify remaining tasks still have their original IDs
    remaining_tasks = list_tasks()
    task_ids = [task["id"] for task in remaining_tasks]
    assert set(task_ids) == {1, 3, 4}  # IDs should be 1, 3, 4 (not 1, 2, 3)

    print("✅ ID persistence after deletion test passed")


def test_empty_list_handling():
    """Test Edge Case: Deleting from Empty List"""
    print("Test Edge Case: Deleting from Empty List")

    # Clear any existing tasks
    TASKS.clear()
    id_generator._current_id = 0

    # Action: Try to delete from empty list
    try:
        delete_task(1)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Task with ID 1 not found" in str(e)
        print("✅ Empty list handling test passed")


def run_all_tests():
    """Run all test cases for Delete Task feature."""
    print("Running Delete Task feature tests...\n")

    test_delete_existing_task()
    test_delete_first_task()
    test_delete_last_task()
    test_delete_only_task()
    test_delete_nonexistent_task()
    test_delete_already_deleted_task()
    test_multiple_sequential_deletes()
    test_id_persistence_after_deletion()
    test_empty_list_handling()

    print("\n🎉 All Delete Task tests passed!")


if __name__ == "__main__":
    run_all_tests()