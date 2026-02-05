# Feature: OpenAI Integration with Function Calling

## Overview
Integrate OpenAI GPT-4o-mini to understand natural language and call appropriate task management functions.

## User Story
As a system, I need to process user's natural language commands through OpenAI and execute the correct task operations.

## Acceptance Criteria

### Must Have
- [ ] OpenAI client initialized with API key
- [ ] Use GPT-4o-mini model (cost-effective)
- [ ] Define 5 function tools (add, list, complete, update, delete)
- [ ] Handle function calling responses
- [ ] Execute called functions
- [ ] Return friendly AI responses
- [ ] Handle errors gracefully
- [ ] Limit conversation history (last 10 messages)
- [ ] Set max_tokens limit for cost control

## Implementation Details

### 1. OpenAI Client Setup

**File:** `backend/app/ai/openai_client.py`

```python
from openai import OpenAI
import os
from typing import List, Dict, Any

# Initialize client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Configuration
OPENAI_MODEL = "gpt-4o-mini"  # Budget-friendly
MAX_TOKENS = 300  # Cost control
TEMPERATURE = 0.7  # Balance creativity/consistency
```

### 2. Function/Tool Definitions

```python
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Create a new task with title and optional description",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Task title (required, 1-200 characters)"
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional task description"
                    }
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "Get list of tasks, optionally filtered by status",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["all", "pending", "completed"],
                        "description": "Filter tasks by status. Default: all"
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Mark a task as complete or toggle completion status",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "ID of the task to mark as complete"
                    }
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "Update task title and/or description",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "ID of the task to update"
                    },
                    "title": {
                        "type": "string",
                        "description": "New title"
                    },
                    "description": {
                        "type": "string",
                        "description": "New description"
                    }
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Delete a task permanently",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "ID of the task to delete"
                    }
                },
                "required": ["task_id"]
            }
        }
    }
]
```

### 3. System Prompt

```python
SYSTEM_PROMPT = """You are a friendly and helpful task management assistant.

Your capabilities:
- Create tasks when users want to remember something
- Show tasks when users ask what they need to do
- Mark tasks complete when users finish them
- Update tasks when users want to change details
- Delete tasks when users no longer need them

Guidelines:
- Be concise and friendly
- Always confirm actions clearly
- When showing tasks, format them nicely
- If a task ID is needed but not provided, ask the user
- Handle errors gracefully with helpful messages

Task display format:
[ID] ☐/✅ Task Title
    Description (if present)
    Created: timestamp
"""
```

### 4. Main Chat Function

```python
def chat_with_ai(
    messages: List[Dict[str, str]],
    user_id: str
) -> Dict[str, Any]:
    """
    Send messages to OpenAI and get response with potential function calls.
    
    Args:
        messages: List of conversation messages
        user_id: Current user ID for function execution
        
    Returns:
        dict with 'content' (text response) and 'tool_calls' (functions called)
    """
    try:
        # Add system prompt
        full_messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            *messages
        ]
        
        # Call OpenAI
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=full_messages,
            tools=TOOLS,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE
        )
        
        message = response.choices[0].message
        
        # Check if AI wants to call functions
        if message.tool_calls:
            return {
                "content": message.content,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "function": tc.function.name,
                        "arguments": json.loads(tc.function.arguments)
                    }
                    for tc in message.tool_calls
                ],
                "requires_function_execution": True
            }
        else:
            # Just a text response
            return {
                "content": message.content,
                "tool_calls": [],
                "requires_function_execution": False
            }
            
    except Exception as e:
        return {
            "content": f"I encountered an error: {str(e)}",
            "tool_calls": [],
            "requires_function_execution": False,
            "error": str(e)
        }
```

### 5. Function Execution

```python
from app.db.queries import tasks as task_queries

def execute_function(
    function_name: str,
    arguments: Dict[str, Any],
    user_id: str,
    db: Session
) -> Dict[str, Any]:
    """
    Execute the called function and return result.
    
    Args:
        function_name: Name of function to call
        arguments: Function arguments from AI
        user_id: User ID for database operations
        db: Database session
        
    Returns:
        Function execution result
    """
    try:
        if function_name == "add_task":
            task = task_queries.create_task(
                db=db,
                user_id=user_id,
                title=arguments["title"],
                description=arguments.get("description", "")
            )
            return {
                "success": True,
                "task_id": task.id,
                "title": task.title,
                "message": f"Task '{task.title}' created successfully"
            }
            
        elif function_name == "list_tasks":
            status = arguments.get("status", "all")
            tasks = task_queries.get_tasks(
                db=db,
                user_id=user_id,
                status=status
            )
            return {
                "success": True,
                "tasks": [
                    {
                        "id": t.id,
                        "title": t.title,
                        "description": t.description,
                        "completed": t.completed,
                        "created_at": t.created_at.isoformat()
                    }
                    for t in tasks
                ],
                "count": len(tasks)
            }
            
        elif function_name == "complete_task":
            task = task_queries.toggle_complete(
                db=db,
                user_id=user_id,
                task_id=arguments["task_id"]
            )
            return {
                "success": True,
                "task_id": task.id,
                "title": task.title,
                "completed": task.completed,
                "message": f"Task '{task.title}' marked as {'complete' if task.completed else 'incomplete'}"
            }
            
        elif function_name == "update_task":
            task = task_queries.update_task(
                db=db,
                user_id=user_id,
                task_id=arguments["task_id"],
                title=arguments.get("title"),
                description=arguments.get("description")
            )
            return {
                "success": True,
                "task_id": task.id,
                "title": task.title,
                "message": f"Task '{task.title}' updated successfully"
            }
            
        elif function_name == "delete_task":
            task = task_queries.delete_task(
                db=db,
                user_id=user_id,
                task_id=arguments["task_id"]
            )
            return {
                "success": True,
                "task_id": task.id,
                "title": task.title,
                "message": f"Task '{task.title}' deleted successfully"
            }
            
        else:
            return {
                "success": False,
                "error": f"Unknown function: {function_name}"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to {function_name}: {str(e)}"
        }
```

### 6. Get Final Response After Function Execution

```python
def get_final_response(
    messages: List[Dict],
    function_results: List[Dict]
) -> str:
    """
    After executing functions, get AI's final response.
    
    Args:
        messages: Original conversation messages
        function_results: Results from executed functions
        
    Returns:
        AI's final response text
    """
    # Add function results to conversation
    tool_messages = []
    for result in function_results:
        tool_messages.append({
            "role": "tool",
            "content": json.dumps(result),
            "tool_call_id": result.get("tool_call_id")
        })
    
    # Get final response
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            *messages,
            *tool_messages
        ],
        max_tokens=MAX_TOKENS
    )
    
    return response.choices[0].message.content
```

## Example Conversation Flow

### Example 1: Add Task

**User:** "Add buy groceries to my list"

**OpenAI Response:**
```json
{
  "tool_calls": [{
    "function": "add_task",
    "arguments": {"title": "Buy groceries"}
  }]
}
```

**After Execution:**
```
✅ Task added successfully!

[1] ⬜ Buy groceries
    Created just now
```

### Example 2: List Tasks

**User:** "What do I need to do today?"

**OpenAI Response:**
```json
{
  "tool_calls": [{
    "function": "list_tasks",
    "arguments": {"status": "pending"}
  }]
}
```

**After Execution:**
```
Here are your pending tasks:

[1] ⬜ Buy groceries
    Created 2 hours ago

[2] ⬜ Call mom
    Description: Birthday wishes
    Created yesterday

You have 2 tasks pending!
```

### Example 3: Complete Task

**User:** "Mark task 1 as done"

**OpenAI Response:**
```json
{
  "tool_calls": [{
    "function": "complete_task",
    "arguments": {"task_id": 1}
  }]
}
```

**After Execution:**
```
✅ Great job! Task completed:

[1] ✅ Buy groceries
```

## Cost Optimization

### Token Usage Per Request

**Typical Request:**
```
System prompt: 100 tokens
User message: 50 tokens
History (10 msgs): 200 tokens
Tools definition: 300 tokens
---
Input total: 650 tokens
Output: 100 tokens
---
Total: 750 tokens ≈ $0.0001 (0.01 cents)
```

### Optimization Strategies

1. **Limit History:**
```python
# Only last 10 messages
messages = messages[-10:]
```

2. **Compact System Prompt:**
```python
# Keep it under 150 tokens
```

3. **Max Tokens Limit:**
```python
max_tokens=300  # Prevent long responses
```

4. **Reuse Tool Definitions:**
```python
# Define once globally, not per request
TOOLS = [...]  # Module level
```

## Error Handling

### Scenarios to Handle

**1. OpenAI API Error:**
```python
try:
    response = client.chat.completions.create(...)
except openai.APIError as e:
    return "I'm having trouble connecting. Please try again."
```

**2. Invalid Function Arguments:**
```python
try:
    task_id = int(arguments["task_id"])
except (KeyError, ValueError):
    return "I need a valid task ID to complete that action."
```

**3. Task Not Found:**
```python
if not task:
    return f"I couldn't find task {task_id}. Try listing your tasks first."
```

**4. Rate Limit:**
```python
except openai.RateLimitError:
    return "I'm a bit overloaded right now. Please wait a moment and try again."
```

## Testing

### Test Cases

**Test 1: Simple Command**
```python
messages = [
    {"role": "user", "content": "Add buy milk"}
]
response = chat_with_ai(messages, "test_user")
assert response["requires_function_execution"] == True
assert response["tool_calls"][0]["function"] == "add_task"
```

**Test 2: Ambiguous Command**
```python
messages = [
    {"role": "user", "content": "Mark it as done"}
]
# Should ask which task
```

**Test 3: Multiple Functions**
```python
messages = [
    {"role": "user", "content": "Add task 1, task 2, and show my list"}
]
# Should call add_task twice, then list_tasks
```

## Files to Create

```
backend/
├── app/
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── openai_client.py       # Main file
│   │   ├── tools.py                # Tool definitions
│   │   └── prompts.py              # System prompts
│   └── .env
│       OPENAI_API_KEY=sk-...
│       OPENAI_MODEL=gpt-4o-mini
```

## Environment Variables

```bash
# .env
OPENAI_API_KEY=sk-proj-xxxxx
OPENAI_MODEL=gpt-4o-mini
OPENAI_MAX_TOKENS=300
OPENAI_TEMPERATURE=0.7
```

## Success Criteria

- [ ] OpenAI client initialized
- [ ] All 5 tools defined correctly
- [ ] System prompt effective
- [ ] Function calling works
- [ ] Function execution works
- [ ] Error handling robust
- [ ] Cost under control (<$0.001 per request)
- [ ] Responses are helpful and friendly

---

**Estimated Time:** 3-4 hours with Qwen
**Priority:** High - Core AI logic
**Dependencies:** Database schema must be ready
