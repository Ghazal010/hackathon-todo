from openai import OpenAI
import os
import json
from typing import List, Dict, Any
from sqlmodel import Session

# Initialize client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Configuration - using gpt-4o-mini as specified in the budget strategy
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")  # Budget-friendly
MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "300"))  # Cost control
TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))  # Balance creativity/consistency


# Define the tools/functions for task management
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
    from .models import Task, TaskCreate
    from datetime import datetime
    import json

    try:
        if function_name == "add_task":
            from .main import task_to_response

            # Create a new task using TaskCreate model
            task_create_data = TaskCreate(
                title=arguments["title"],
                completed=False,
                priority="medium",
                tags=[],  # Empty tags list
                due_date=arguments.get("description")
            )

            # Convert user_id to integer for the new schema
            user_id_int = int(user_id)

            # Create task object with user_id
            new_task = Task(
                title=task_create_data.title,
                completed=task_create_data.completed,
                priority=task_create_data.priority,
                tags=json.dumps(task_create_data.tags) if task_create_data.tags else "[]",
                due_date=task_create_data.due_date,
                user_id=user_id_int  # Use the converted user_id
            )

            db.add(new_task)
            db.commit()
            db.refresh(new_task)

            task_response = task_to_response(new_task)

            return {
                "success": True,
                "task_id": task_response.id,
                "title": task_response.title,
                "message": f"Task '{task_response.title}' created successfully"
            }

        elif function_name == "list_tasks":
            from .main import task_to_response
            from sqlmodel import select

            status = arguments.get("status", "all")

            # Convert user_id to integer for the new schema
            user_id_int = int(user_id)

            # Build query based on status and user_id
            query = select(Task).where(Task.user_id == user_id_int)

            if status == "pending":
                query = query.where(Task.completed == False)
            elif status == "completed":
                query = query.where(Task.completed == True)

            tasks = db.exec(query).all()

            return {
                "success": True,
                "tasks": [
                    {
                        "id": t.id,
                        "title": t.title,
                        "description": t.due_date,  # Using due_date as description for now
                        "completed": t.completed,
                        "created_at": t.created_at.isoformat()
                    }
                    for t in tasks
                ],
                "count": len(tasks)
            }

        elif function_name == "complete_task":
            from .main import task_to_response
            from sqlmodel import select

            # Convert user_id to integer for the new schema
            user_id_int = int(user_id)

            # Find task by ID and user_id
            query = select(Task).where(Task.id == arguments["task_id"]).where(Task.user_id == user_id_int)
            task = db.exec(query).first()

            if not task:
                return {
                    "success": False,
                    "error": f"Task {arguments['task_id']} not found",
                    "message": f"Task {arguments['task_id']} not found"
                }

            # Toggle completion
            task.completed = not task.completed
            task.updated_at = datetime.utcnow()
            db.add(task)
            db.commit()
            db.refresh(task)

            task_response = task_to_response(task)

            return {
                "success": True,
                "task_id": task_response.id,
                "title": task_response.title,
                "completed": task_response.completed,
                "message": f"Task '{task_response.title}' marked as {'complete' if task_response.completed else 'incomplete'}"
            }

        elif function_name == "update_task":
            from .main import task_to_response
            from sqlmodel import select

            # Convert user_id to integer for the new schema
            user_id_int = int(user_id)

            # Find task by ID and user_id
            query = select(Task).where(Task.id == arguments["task_id"]).where(Task.user_id == user_id_int)
            task = db.exec(query).first()

            if not task:
                return {
                    "success": False,
                    "error": f"Task {arguments['task_id']} not found",
                    "message": f"Task {arguments['task_id']} not found"
                }

            # Update task fields
            if "title" in arguments and arguments["title"]:
                task.title = arguments["title"]
            if "description" in arguments and arguments["description"] is not None:
                task.due_date = arguments["description"]  # Using due_date as description for now

            task.updated_at = datetime.utcnow()
            db.add(task)
            db.commit()
            db.refresh(task)

            task_response = task_to_response(task)

            return {
                "success": True,
                "task_id": task_response.id,
                "title": task_response.title,
                "message": f"Task '{task_response.title}' updated successfully"
            }

        elif function_name == "delete_task":
            from .main import task_to_response
            from sqlmodel import select

            # Convert user_id to integer for the new schema
            user_id_int = int(user_id)

            # Find task by ID and user_id
            query = select(Task).where(Task.id == arguments["task_id"]).where(Task.user_id == user_id_int)
            task = db.exec(query).first()

            if not task:
                return {
                    "success": False,
                    "error": f"Task {arguments['task_id']} not found",
                    "message": f"Task {arguments['task_id']} not found"
                }

            # Delete task
            db.delete(task)
            db.commit()

            task_response = task_to_response(task)

            return {
                "success": True,
                "task_id": task_response.id,
                "title": task_response.title,
                "message": f"Task '{task_response.title}' deleted successfully"
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