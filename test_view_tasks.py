#!/usr/bin/env python3
"""Test script for the View Tasks feature."""

import sys
import os
# Add the project root to the Python path to allow imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.task_manager import add_task, list_tasks, TASKS
from src.utils import display_tasks
from src.utils import id_generator


def test_view_empty_list():
    """Test 1: View Empty List"""
    print("Test 1: View Empty List")

    # Clear any existing tasks
    TASKS.clear()
    id_generator._current_id = 0

    tasks = list_tasks()
    assert len(tasks) == 0, f"Expected empty list, got {tasks}"
    print("✅ Empty list test passed")


def test_view_single_task():
    """Test 2: View Single Task"""
    print("Test 2: View Single Task")

    # Clear any existing tasks
    TASKS.clear()
    id_generator._current_id = 0

    # Add a single task
    add_task("Buy groceries")

    tasks = list_tasks()
    assert len(tasks) == 1, f"Expected 1 task, got {len(tasks)}"
    assert tasks[0]["title"] == "Buy groceries", f"Expected 'Buy groceries', got {tasks[0]['title']}"
    assert tasks[0]["completed"] is False, f"Expected False, got {tasks[0]['completed']}"
    print("✅ Single task test passed")


def test_view_multiple_tasks():
    """Test 3: View Multiple Tasks"""
    print("Test 3: View Multiple Tasks")

    # Clear any existing tasks
    TASKS.clear()
    id_generator._current_id = 0

    # Add multiple tasks
    task1 = add_task("Buy groceries", "Milk, eggs, bread")
    task2 = add_task("Call mom", "Birthday wishes")
    task3 = add_task("Finish report")

    tasks = list_tasks()
    assert len(tasks) == 3, f"Expected 3 tasks, got {len(tasks)}"

    # Check each task
    assert tasks[0]["id"] == 1
    assert tasks[0]["title"] == "Buy groceries"
    assert tasks[0]["description"] == "Milk, eggs, bread"

    assert tasks[1]["id"] == 2
    assert tasks[1]["title"] == "Call mom"
    assert tasks[1]["description"] == "Birthday wishes"

    assert tasks[2]["id"] == 3
    assert tasks[2]["title"] == "Finish report"
    assert tasks[2]["description"] == ""

    print("✅ Multiple tasks test passed")


def test_display_tasks_function():
    """Test the display_tasks function manually by checking it doesn't crash"""
    print("Test: Display Tasks Function")

    # Clear any existing tasks
    TASKS.clear()
    id_generator._current_id = 0

    # Add a task and try to display it
    add_task("Test task", "Test description")
    tasks = list_tasks()

    # This should not raise an exception
    try:
        display_tasks(tasks)
        print("✅ Display tasks function works without crashing")
    except Exception as e:
        print(f"❌ Display tasks function failed: {e}")
        raise


def test_display_empty_tasks():
    """Test displaying empty tasks list"""
    print("Test: Display Empty Tasks")

    # Clear any existing tasks
    TASKS.clear()
    id_generator._current_id = 0

    tasks = list_tasks()
    assert len(tasks) == 0

    # This should not raise an exception
    try:
        display_tasks(tasks)
        print("✅ Display empty tasks works without crashing")
    except Exception as e:
        print(f"❌ Display empty tasks failed: {e}")
        raise


def run_all_tests():
    """Run all test cases for View Tasks feature."""
    print("Running View Tasks feature tests...\n")

    test_view_empty_list()
    test_view_single_task()
    test_view_multiple_tasks()
    test_display_empty_tasks()
    test_display_tasks_function()

    print("\n🎉 All View Tasks tests passed!")


if __name__ == "__main__":
    run_all_tests()