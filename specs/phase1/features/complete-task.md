Feature: Mark Task Complete/Incomplete
User Story
As a user, I want to mark tasks as complete or incomplete so that I can track my progress.
Acceptance Criteria
Must Have

 User can toggle task completion status by ID
 If task is incomplete, mark it complete
 If task is complete, mark it incomplete (toggle)
 Show success message with new status
 Show error if task ID not found
 Task ID must be a positive integer

Validation Rules

 Task ID must exist in the list
 Show error: "Task with ID {id} not found" if invalid
 Handle non-numeric input gracefully

Implementation Details
Function Signature
pythondef toggle_task_complete(task_id: int) -> dict:
    """
    Toggle the completion status of a task.
    
    Args:
        task_id: ID of the task to toggle
        
    Returns:
        dict: Updated task with new completion status
        
    Raises:
        ValueError: If task_id not found
    """
Behavior

Find task by ID
Flip completed field: False → True or True → False
Return updated task
Raise error if task not found

CLI Interaction Flow
Success Case - Mark Complete
Choose option (1-6): 5

Enter task ID: 1

✅ Task marked as complete!
   [1] ✅ Buy groceries

Press Enter to continue...
Success Case - Mark Incomplete
Choose option (1-6): 5

Enter task ID: 1

✅ Task marked as incomplete!
   [1] ⬜ Buy groceries

Press Enter to continue...
Error Case - Task Not Found
Choose option (1-6): 5

Enter task ID: 999

❌ Error: Task with ID 999 not found

Press Enter to continue...
Error Case - Invalid Input
Choose option (1-6): 5

Enter task ID: abc

❌ Error: Please enter a valid task ID (number)

Press Enter to continue...
Test Cases
Test 1: Mark Incomplete Task as Complete
Setup:

Add task: "Buy groceries" (ID: 1, completed: False)

Action:

Toggle task 1

Expected:

Task 1 completed: True
Success message shown
Task shows as ✅ in View Tasks

Test 2: Mark Complete Task as Incomplete
Setup:

Task 1 is complete (completed: True)

Action:

Toggle task 1 again

Expected:

Task 1 completed: False
Success message shown
Task shows as ⬜ in View Tasks

Test 3: Multiple Toggles
Setup:

Task 1 incomplete

Action:

Toggle 5 times

Expected:

After odd toggles (1,3,5): complete
After even toggles (2,4): incomplete
Each toggle works correctly

Test 4: Invalid Task ID
Setup:

Tasks exist with IDs 1, 2, 3

Action:

Try to toggle task ID 999

Expected:

ValueError raised
Error message: "Task with ID 999 not found"
No tasks modified

Test 5: Toggle After Deletion
Setup:

Add tasks 1, 2, 3
Delete task 2
Try to toggle task 2

Expected:

Error: "Task with ID 2 not found"
Tasks 1 and 3 unchanged

Test 6: Non-numeric Input
Setup:

Normal state

Action:

Enter "abc" as task ID

Expected:

Graceful error handling
Error message about invalid input
App doesn't crash

Edge Cases to Handle

Negative Task ID: Should show error (IDs start from 1)
Zero Task ID: Should show error
Float Input: Should show error or convert to int
Empty Input: Should prompt again or show error

CLI Enhancement (Optional)
Show task details when toggling:
✅ Task marked as complete!
   [1] ✅ Buy groceries
       Description: Milk, eggs, bread
Dependencies

Depends on: Add Task (need tasks to complete)
Works with: View Tasks (status should update)

Files to Modify/Create

src/task_manager.py - toggle_task_complete() function
src/main.py - CLI menu option 5

Success Criteria

 All test cases pass
 Toggle works both ways (complete ↔ incomplete)
 Error handling for invalid IDs
 Success messages are clear
 Status visible in View Tasks immediately
 No crashes on invalid input


Priority: High - Implement third
Estimated Time: 20-30 minutes with Qwen
