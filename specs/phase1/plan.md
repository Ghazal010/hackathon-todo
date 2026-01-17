# Feature: Add Task

## User Story
As a user, I want to add a new task with a title and optional description so that I can track things I need to do.

## Acceptance Criteria

### Must Have
- [ ] User can create a task with a title
- [ ] Title is required (cannot be empty)
- [ ] Title must be 1-200 characters long
- [ ] Description is optional
- [ ] Description can be up to 1000 characters
- [ ] Each task automatically gets a unique ID
- [ ] New tasks default to "incomplete" status
- [ ] Task creation timestamp is automatically recorded
- [ ] Success message shown after task is added

### Validation Rules
- [ ] Empty title shows error: "Title cannot be empty"
- [ ] Title > 200 chars shows error: "Title too long (max 200 characters)"
- [ ] Description > 1000 chars shows error: "Description too long (max 1000 characters)"
- [ ] Whitespace-only titles are rejected

## Implementation Details

### Function Signature
```python
def add_task(title: str, description: str = "") -> dict:
    """
    Add a new task to the task list.
    
    Args:
        title: Task title (required, 1-200 characters)
        description: Task description (optional, max 1000 characters)
        
    Returns:
        dict: Created task with id, title, description, completed, created_at
        
    Raises:
        ValueError: If title is invalid or description too long
    """
```

### Task Structure
```python
{
    "id": int,                    # Unique, auto-generated
    "title": str,                 # Required, 1-200 chars
    "description": str,           # Optional, max 1000 chars
    "completed": bool,            # Default: False
    "created_at": str            # ISO format timestamp
}
```

### ID Generation
- Use a simple counter that increments with each task
- Start from 1
- Never reuse IDs (even after deletion)

### Timestamp Format
- Use ISO 8601 format: `2025-12-01T10:30:00`
- Use `datetime.now().isoformat()`

## CLI Interaction Flow

### Success Case
```
Choose option (1-6): 1

Enter task title: Buy groceries
Enter description (optional): Milk, eggs, bread

✅ Task added successfully! (ID: 1)
```

### Error Case - Empty Title
```
Choose option (1-6): 1

Enter task title: 
❌ Error: Title cannot be empty

Press Enter to continue...
```

### Error Case - Title Too Long
```
Choose option (1-6): 1

Enter task title: [201+ characters]
❌ Error: Title too long (max 200 characters)

Press Enter to continue...
```

## Test Cases

### Test 1: Add Task with Title Only
**Input:**
- Title: "Buy groceries"
- Description: (empty)

**Expected:**
- Task created with ID 1
- Title: "Buy groceries"
- Description: ""
- Completed: False
- created_at: Current timestamp

### Test 2: Add Task with Title and Description
**Input:**
- Title: "Call mom"
- Description: "Birthday wishes"

**Expected:**
- Task created with ID 2
- Both title and description stored
- Status: incomplete

### Test 3: Empty Title Rejected
**Input:**
- Title: ""

**Expected:**
- ValueError raised
- Error message: "Title cannot be empty"
- No task created

### Test 4: Whitespace-Only Title Rejected
**Input:**
- Title: "   "

**Expected:**
- ValueError raised
- Error message: "Title cannot be empty"
- No task created

### Test 5: Title Too Long Rejected
**Input:**
- Title: (201 characters)

**Expected:**
- ValueError raised
- Error message contains "max 200 characters"
- No task created

### Test 6: Description Too Long Rejected
**Input:**
- Title: "Valid title"
- Description: (1001 characters)

**Expected:**
- ValueError raised
- Error message contains "max 1000 characters"
- No task created

### Test 7: Multiple Tasks Get Unique IDs
**Input:**
- Add task 1: "Task One"
- Add task 2: "Task Two"
- Add task 3: "Task Three"

**Expected:**
- Task 1 has ID: 1
- Task 2 has ID: 2
- Task 3 has ID: 3
- All IDs are unique

## Edge Cases to Handle

1. **Very Long Valid Title**: Exactly 200 characters should work
2. **Very Long Valid Description**: Exactly 1000 characters should work
3. **Special Characters**: Title/description with emojis, unicode should work
4. **Newlines in Description**: Should be allowed
5. **Leading/Trailing Whitespace**: Should be trimmed from title

## Dependencies
- None (first feature to implement)

## Files to Modify/Create
- `src/models.py` - Task type definition
- `src/task_manager.py` - add_task() function
- `src/utils.py` - ID generation, timestamp helpers
- `src/main.py` - CLI menu option 1

## Success Criteria
- [ ] All test cases pass
- [ ] Code has type hints
- [ ] Code has docstrings
- [ ] Input validation works
- [ ] Error messages are clear
- [ ] Task is visible in "View All Tasks" after creation

---

**Priority**: High - Implement this first
**Estimated Time**: 30-45 minutes with Qwen
