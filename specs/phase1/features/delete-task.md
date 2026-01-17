Feature: Delete Task
User Story
As a user, I want to delete tasks that I no longer need so that my task list stays clean and relevant.

Acceptance Criteria
Must Have
 User can delete task by ID
 Task is permanently removed from the list
 Show confirmation message with deleted task details
 Show error if task ID not found
 Handle empty list gracefully
 Other task IDs remain unchanged (no renumbering)
Optional but Recommended
 Ask for confirmation before deleting
 Show task details before deletion
Implementation Details
Function Signature
python
def delete_task(task_id: int) -> dict:
    """
    Delete a task from the task list.
    
    Args:
        task_id: ID of the task to delete
        
    Returns:
        dict: The deleted task (for confirmation message)
        
    Raises:
        ValueError: If task_id not found
    """
Delete Logic
Find task by ID
Remove from task list
Return deleted task (for showing confirmation)
Raise error if not found
Do NOT renumber remaining task IDs
CLI Interaction Flow
Success Case - Simple Delete
Choose option (1-6): 4

Enter task ID to delete: 2

✅ Task deleted successfully!
   Deleted: [2] Buy groceries
            Description: Milk, eggs

Press Enter to continue...
Success Case - With Confirmation
Choose option (1-6): 4

Enter task ID to delete: 2

Task to delete:
[2] ✅ Buy groceries
    Description: Milk, eggs, bread

Are you sure you want to delete this task? (y/n): y

✅ Task deleted successfully!

Press Enter to continue...
Cancel Deletion
Are you sure you want to delete this task? (y/n): n

❌ Deletion cancelled. Task not deleted.

Press Enter to continue...
Error Case - Task Not Found
Choose option (1-6): 4

Enter task ID to delete: 999

❌ Error: Task with ID 999 not found

Press Enter to continue...
Error Case - Empty List
Choose option (1-6): 4

❌ No tasks to delete. Your task list is empty.

Press Enter to continue...
Test Cases
Test 1: Delete Existing Task
Setup:

Tasks: 1, 2, 3
Action:

Delete task 2
Expected:

Task 2 removed from list
Tasks 1 and 3 still exist
IDs remain 1 and 3 (NOT renumbered to 1 and 2)
Success message shown
Test 2: Delete First Task
Setup:

Tasks: 1, 2, 3
Action:

Delete task 1
Expected:

Task 1 removed
Tasks 2 and 3 remain with IDs 2 and 3
No renumbering
Test 3: Delete Last Task
Setup:

Tasks: 1, 2, 3
Action:

Delete task 3
Expected:

Task 3 removed
Tasks 1 and 2 remain unchanged
Test 4: Delete Only Task
Setup:

Only task 1 exists
Action:

Delete task 1
Expected:

Task list becomes empty
View Tasks shows "No tasks found"
Can add new task (will get ID 2, not reuse 1)
Test 5: Delete Non-existent Task
Setup:

Tasks: 1, 2, 3
Action:

Try to delete task 5
Expected:

ValueError raised
Error message: "Task with ID 5 not found"
No tasks deleted
Test 6: Delete Already Deleted Task
Setup:

Task 2 was deleted earlier
Action:

Try to delete task 2 again
Expected:

Error: "Task with ID 2 not found"
Other tasks unchanged
Test 7: Multiple Sequential Deletes
Setup:

Tasks: 1, 2, 3, 4, 5
Action:

Delete 2, then delete 4, then delete 1
Expected:

Remaining tasks: 3, 5
IDs remain unchanged
Each deletion shows correct confirmation
Edge Cases to Handle
Deleting from Empty List: Should show appropriate message
Invalid Input (non-numeric): Should handle gracefully
Negative Task ID: Should show error
Task ID 0: Should show error
Confirmation Dialog (Recommended)
Simple Confirmation
python
response = input("Are you sure? (y/n): ").lower().strip()
if response != 'y':
    print("Deletion cancelled.")
    return
Detailed Confirmation
python
print(f"\nYou are about to delete:")
display_task(task)
response = input("\nThis action cannot be undone. Continue? (y/n): ")
Important Implementation Notes
DO NOT Renumber IDs
❌ Wrong:

python
# After deleting task 2 from [1,2,3]:
# Tasks become [1,2] ← Task 3 was renumbered to 2 (WRONG!)
✅ Correct:

python
# After deleting task 2 from [1,2,3]:
# Tasks remain [1,3] ← IDs unchanged
Why?
IDs should be permanent identifiers
Users might reference IDs elsewhere
Prevents confusion
Prepares for Phase 2 (database will work this way)
Dependencies
Depends on: Add Task (need tasks to delete)
Works with: View Tasks (deleted tasks shouldn't appear)
Works with: Update/Complete (deleted IDs should error)
Files to Modify/Create
src/task_manager.py - delete_task() function
src/main.py - CLI menu option 4
Success Criteria
 All test cases pass
 Task permanently removed
 IDs NOT renumbered after deletion
 Error handling for invalid IDs
 Confirmation message shows deleted task details
 Works with empty list
 No crashes on invalid input
Priority: Medium - Implement fifth (last basic feature) Estimated Time: 20-30 minutes with Qwen

