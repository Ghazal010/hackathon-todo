Feature: Update Task
User Story
As a user, I want to update a task's title and/or description so that I can correct mistakes or add more details.
Acceptance Criteria
Must Have

 User can update task by ID
 User can update title only
 User can update description only
 User can update both title and description
 New title must follow same validation rules (1-200 chars)
 New description must follow same rules (max 1000 chars)
 Show error if task ID not found
 Show success message after update
 Display updated task details

Validation Rules

 Same validation as Add Task:

Title: 1-200 characters, not empty
Description: max 1000 characters


 At least one field must be updated
 Whitespace-only updates rejected

Implementation Details
Function Signature
pythondef update_task(
    task_id: int,
    title: str | None = None,
    description: str | None = None
) -> dict:
    """
    Update a task's title and/or description.
    
    Args:
        task_id: ID of the task to update
        title: New title (optional, must be valid if provided)
        description: New description (optional)
        
    Returns:
        dict: Updated task
        
    Raises:
        ValueError: If task_id not found or validation fails
    """
Update Logic

Find task by ID
If title provided: validate and update
If description provided: update
If both None: raise error (nothing to update)
Return updated task

CLI Interaction Flow
Case 1: Update Title Only
Choose option (1-6): 3

Enter task ID: 1

Current task:
[1] ⬜ Buy groceries
    Description: Milk, eggs

Update title (press Enter to keep current): Buy groceries and fruits
Update description (press Enter to keep current): 

✅ Task updated successfully!
   [1] ⬜ Buy groceries and fruits
       Description: Milk, eggs

Press Enter to continue...
Case 2: Update Description Only
Choose option (1-6): 3

Enter task ID: 1

Current task:
[1] ⬜ Buy groceries
    Description: Milk, eggs

Update title (press Enter to keep current): 
Update description (press Enter to keep current): Milk, eggs, bread, butter

✅ Task updated successfully!
   [1] ⬜ Buy groceries
       Description: Milk, eggs, bread, butter

Press Enter to continue...
Case 3: Update Both
Choose option (1-6): 3

Enter task ID: 1

Current task:
[1] ⬜ Buy groceries
    Description: Milk, eggs

Update title (press Enter to keep current): Weekly grocery shopping
Update description (press Enter to keep current): Milk, eggs, bread, fruits

✅ Task updated successfully!
   [1] ⬜ Weekly grocery shopping
       Description: Milk, eggs, bread, fruits

Press Enter to continue...
Error Case - Task Not Found
Choose option (1-6): 3

Enter task ID: 999

❌ Error: Task with ID 999 not found

Press Enter to continue...
Error Case - Invalid Title
Choose option (1-6): 3

Enter task ID: 1

Update title (press Enter to keep current): [201+ characters]

❌ Error: Title too long (max 200 characters)

Press Enter to continue...
Error Case - No Changes
Choose option (1-6): 3

Enter task ID: 1

Update title (press Enter to keep current): 
Update description (press Enter to keep current): 

❌ Error: No changes provided. Task remains unchanged.

Press Enter to continue...
Test Cases
Test 1: Update Title Only
Setup:

Task 1: "Buy groceries", description: "Milk"

Action:

Update title to: "Buy weekly groceries"
Leave description empty (keep current)

Expected:

Title changed to "Buy weekly groceries"
Description still "Milk"
Success message shown

Test 2: Update Description Only
Setup:

Task 1: "Buy groceries", description: "Milk"

Action:

Leave title empty (keep current)
Update description to: "Milk, eggs, bread"

Expected:

Title still "Buy groceries"
Description changed to "Milk, eggs, bread"
Success message shown

Test 3: Update Both Fields
Setup:

Task 1: "Buy groceries", description: "Milk"

Action:

Update title to: "Shopping"
Update description to: "Weekly shopping list"

Expected:

Both fields updated
Success message shown

Test 4: Update to Empty Description
Setup:

Task 1 has description: "Some text"

Action:

Update description to: ""

Expected:

Description cleared (becomes "")
This is allowed
Title unchanged

Test 5: Invalid Title Update
Setup:

Task 1 exists

Action:

Try to update title to empty string or 201+ chars

Expected:

ValueError raised
Error message shown
Task unchanged

Test 6: Update Non-existent Task
Setup:

Only tasks 1, 2, 3 exist

Action:

Try to update task 5

Expected:

ValueError raised
Error message: "Task with ID 5 not found"

Test 7: No Changes Provided
Setup:

Task 1 exists

Action:

Press Enter for both title and description (no changes)

Expected:

Error or info message
Task unchanged

Edge Cases to Handle

Whitespace-only Title: Should be rejected like empty title
Very Long Valid Updates: Exactly 200 chars title, 1000 chars description should work
Special Characters: Should work in both title and description
Task Completion Status: Should remain unchanged after update

CLI Enhancement (Optional)
Show "before and after" view:
Before:
[1] ⬜ Buy groceries
    Description: Milk

After:
[1] ⬜ Buy groceries and fruits
    Description: Milk, eggs, bread
Dependencies

Depends on: Add Task (need tasks to update)
Works with: View Tasks (updates should be visible)

Files to Modify/Create

src/task_manager.py - update_task() function
src/main.py - CLI menu option 3

Success Criteria

 All test cases pass
 Can update title only
 Can update description only
 Can update both
 Validation works same as Add Task
 Error handling for invalid IDs
 Clear success/error messages
 Completion status unchanged


Priority: Medium - Implement fourth
Estimated Time: 25-35 minutes with Qwen
