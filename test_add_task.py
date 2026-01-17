#!/usr/bin/env python3
"""Test script for the Add Task feature."""

import sys
import os
# Add the project root to the Python path to allow imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.task_manager import add_task
from src.utils import IdGenerator


def test_add_task_with_title_only():
    """Test 1: Add Task with Title Only"""
    print("Test 1: Add Task with Title Only")
    task = add_task("Buy groceries")

    assert task["title"] == "Buy groceries"
    assert task["description"] == ""
    assert task["completed"] is False
    assert "created_at" in task
    assert isinstance(task["id"], int)
    print("✅ Passed")


def test_add_task_with_title_and_description():
    """Test 2: Add Task with Title and Description"""
    print("Test 2: Add Task with Title and Description")
    task = add_task("Call mom", "Birthday wishes")

    assert task["title"] == "Call mom"
    assert task["description"] == "Birthday wishes"
    assert task["completed"] is False
    assert "created_at" in task
    assert isinstance(task["id"], int)
    print("✅ Passed")


def test_empty_title_rejected():
    """Test 3: Empty Title Rejected"""
    print("Test 3: Empty Title Rejected")
    try:
        add_task("")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "cannot be empty" in str(e)
        print("✅ Passed")


def test_whitespace_only_title_rejected():
    """Test 4: Whitespace-Only Title Rejected"""
    print("Test 4: Whitespace-Only Title Rejected")
    try:
        add_task("   ")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "cannot be empty" in str(e)
        print("✅ Passed")


def test_title_too_long_rejected():
    """Test 5: Title Too Long Rejected"""
    print("Test 5: Title Too Long Rejected")
    long_title = "a" * 201  # 201 characters
    try:
        add_task(long_title)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "max 200 characters" in str(e)
        print("✅ Passed")


def test_description_too_long_rejected():
    """Test 6: Description Too Long Rejected"""
    print("Test 6: Description Too Long Rejected")
    long_desc = "a" * 1001  # 1001 characters
    try:
        add_task("Valid title", long_desc)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "max 1000 characters" in str(e)
        print("✅ Passed")


def test_multiple_tasks_get_unique_ids():
    """Test 7: Multiple Tasks Get Unique IDs"""
    print("Test 7: Multiple Tasks Get Unique IDs")
    # Reset ID generator to start from 1 for this test
    from src.utils import id_generator
    id_generator._current_id = 0

    task1 = add_task("Task One")
    task2 = add_task("Task Two")
    task3 = add_task("Task Three")

    assert task1["id"] == 1
    assert task2["id"] == 2
    assert task3["id"] == 3
    print("✅ Passed")


def test_very_long_valid_title():
    """Edge Case: Very Long Valid Title (exactly 200 characters)"""
    print("Edge Case: Very Long Valid Title (exactly 200 characters)")
    long_title = "a" * 200  # Exactly 200 characters
    task = add_task(long_title)
    assert task["title"] == long_title
    print("✅ Passed")


def test_very_long_valid_description():
    """Edge Case: Very Long Valid Description (exactly 1000 characters)"""
    print("Edge Case: Very Long Valid Description (exactly 1000 characters)")
    long_desc = "a" * 1000  # Exactly 1000 characters
    task = add_task("Valid title", long_desc)
    assert task["description"] == long_desc
    print("✅ Passed")


def test_special_characters():
    """Edge Case: Special Characters (emojis, unicode)"""
    print("Edge Case: Special Characters (emojis, unicode)")
    task = add_task("Task with emoji 🚀", "Unicode: café résumé naïve")
    assert task["title"] == "Task with emoji 🚀"
    assert task["description"] == "Unicode: café résumé naïve"
    print("✅ Passed")


def test_newlines_in_description():
    """Edge Case: Newlines in Description"""
    print("Edge Case: Newlines in Description")
    desc_with_newlines = "Line 1\nLine 2\nLine 3"
    task = add_task("Task with newlines", desc_with_newlines)
    assert task["description"] == desc_with_newlines
    print("✅ Passed")


def test_leading_trailing_whitespace_trimmed():
    """Edge Case: Leading/Trailing Whitespace Trimmed from Title"""
    print("Edge Case: Leading/Trailing Whitespace Trimmed from Title")
    task = add_task("  Title with spaces  ", "Description")
    assert task["title"] == "Title with spaces"
    print("✅ Passed")


def run_all_tests():
    """Run all test cases."""
    print("Running Add Task feature tests...\n")

    test_add_task_with_title_only()
    test_add_task_with_title_and_description()
    test_empty_title_rejected()
    test_whitespace_only_title_rejected()
    test_title_too_long_rejected()
    test_description_too_long_rejected()
    test_multiple_tasks_get_unique_ids()
    test_very_long_valid_title()
    test_very_long_valid_description()
    test_special_characters()
    test_newlines_in_description()
    test_leading_trailing_whitespace_trimmed()

    print("\n🎉 All tests passed!")


if __name__ == "__main__":
    run_all_tests()