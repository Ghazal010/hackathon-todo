Feature: View All Tasks
User Story
As a user, I want to see all my tasks in a readable format so that I can review what I need to do.
Acceptance Criteria
Must Have

 Display all tasks in the list
 Show task ID for each task
 Show task title
 Show completion status (✅ or ⬜)
 Show creation timestamp
 Show description (if present)
 Handle empty task list gracefully
 Format output in a clean, readable way

Display Format

 Tasks separated visually (blank lines or dividers)
 Completed tasks marked with ✅
 Incomplete tasks marked with ⬜
 Timestamps in human-readable format
 Long descriptions don't break layout

Implementation Details
Function Signature
pythondef list_tasks() -> list[dict]:
    """
    Get all tasks from the task list.
    
    Returns:
        list[dict]: List of all tasks, or empty list if none exist
    """
Display Function
pythondef display_tasks(tasks: list[dict]) -> None:
    """
    Display tasks in a formatted, readable way.
    
    Args:
        tasks: List of task dictionaries to display
    """
CLI Interaction Flow
Case 1: Tasks Exist
Choose option (1-6): 2

=== All Tasks ===

[1] ⬜ Buy groceries
    Created: 2025-12-01 10:30
    Description: Milk, eggs, bread

[2] ✅ Call mom
    Created: 2025-12-01 09:15
    Description: Birthday wishes

[3] ⬜ Finish report
    Created: 2025-12-01 11:00
    Description: 

Total: 3 tasks (1 completed, 2 pending)

Press Enter to continue...
Case 2: No Tasks
Choose option (1-6): 2

=== All Tasks ===

No tasks found. Add your first task!

Press Enter to continue...
Case 3: Only Completed Tasks
Choose option (1-6): 2

=== All Tasks ===

[1] ✅ Buy groceries
    Created: 2025-12-01 10:30
    Description: Milk, eggs, bread

[2] ✅ Call mom
    Created: 2025-12-01 09:15
    Description: 

Total: 2 tasks (2 completed, 0 pending)

Press Enter to continue...
Test Cases
Test 1: View Empty List
Setup:

No tasks added

Expected Output:
=== All Tasks ===

No tasks found. Add your first task!
Test 2: View Single Task
Setup:

Add task: "Buy groceries"

Expected Output:
[1] ⬜ Buy groceries
    Created: [timestamp]
    Description: 

Total: 1 task (0 completed, 1 pending)
Test 3: View Multiple Tasks
Setup:

Add 3 tasks (mix of complete/incomplete)

Expected:

All 3 tasks shown
Correct IDs
Correct status icons
Summary line shows correct counts

Test 4: View After Task Deletion
Setup:

Add 3 tasks
Delete task ID 2
View tasks

Expected:

Only tasks 1 and 3 shown
Task 2 not in list
IDs remain unchanged (1 and 3, not renumbered)

Test 5: View Tasks with Long Descriptions
Setup:

Add task with 500-character description

Expected:

Description displays completely
No layout breaking
Readable format

Test 6: View Tasks in Order
Setup:

Add tasks in order: A, B, C

Expected:

Tasks display in creation order
Oldest first (A, then B, then C)

Edge Cases to Handle

Very Long Title: Should display fully without breaking layout
Empty Description: Should show cleanly (no "Description: " line or empty line)
Special Characters: Emojis and unicode should display correctly
Many Tasks: Should handle 50+ tasks without breaking

Formatting Guidelines
Status Icons

Incomplete: ⬜ or [ ]
Complete: ✅ or [✓]

Timestamp Format

ISO to readable: 2025-12-01T10:30:00 → 2025-12-01 10:30
Or use: Dec 01, 2025 at 10:30 AM

Description Display

If empty: Don't show "Description:" line at all
If present: Show on separate indented line
If very long: Display all (no truncation)

Dependencies

Depends on: Add Task feature (must have tasks to view)

Files to Modify/Create

src/task_manager.py - list_tasks() function
src/utils.py - display_tasks() formatting function
src/main.py - CLI menu option 2

Success Criteria

 All test cases pass
 Empty list handled gracefully
 Output is clean and readable
 Status icons display correctly
 Task count summary is accurate
 Works with tasks created, updated, or completed


Priority: High - Implement second (after Add Task)
Estimated Time: 20-30 minutes with Qwen
