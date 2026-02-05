# Feature: Chat API Endpoint

## Overview
Create a RESTful endpoint that receives user messages, processes them through OpenAI, executes functions, and returns AI responses.

## User Story
As a frontend application, I need an API endpoint to send user chat messages and receive AI responses with task operation results.

## Acceptance Criteria

### Must Have
- [ ] POST endpoint at `/api/{user_id}/chat`
- [ ] Accept message and optional conversation_id
- [ ] Create new conversation if none provided
- [ ] Fetch conversation history (last 10 messages)
- [ ] Send to OpenAI with history
- [ ] Execute any function calls
- [ ] Store user message and AI response
- [ ] Return AI response to client
- [ ] Handle errors gracefully
- [ ] Stateless server (no in-memory state)

## API Specification

### Endpoint

```
POST /api/{user_id}/chat
```

### Request

**Path Parameters:**
- `user_id` (string, required): User's email or ID from Better Auth

**Body:**
```json
{
  "message": "Add buy groceries to my list",
  "conversation_id": 123  // Optional, creates new if not provided
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/ghazal@example.com/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "message": "Show me my tasks",
    "conversation_id": 1
  }'
```

### Response

**Success (200):**
```json
{
  "conversation_id": 1,
  "message_id": 45,
  "response": "Here are your tasks:\n\n[1] ⬜ Buy groceries\n    Created 2 hours ago\n\n[2] ✅ Call mom\n    Completed today",
  "tool_calls": [
    {
      "function": "list_tasks",
      "arguments": {"status": "all"},
      "result": {
        "success": true,
        "tasks": [...],
        "count": 2
      }
    }
  ]
}
```

**Error (400/500):**
```json
{
  "detail": "Error message here",
  "conversation_id": 1
}
```

## Implementation

### File Structure

```
backend/
├── app/
│   ├── routes/
│   │   └── chat.py            # This file
│   ├── schemas/
│   │   └── chat.py            # Request/Response models
│   ├── ai/
│   │   └── openai_client.py   # AI functions
│   └── db/
│       └── queries/
│           └── chat.py         # DB operations
```

### 1. Pydantic Schemas

**File:** `backend/app/schemas/chat.py`

```python
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)
    conversation_id: Optional[int] = None

class ToolCall(BaseModel):
    function: str
    arguments: Dict[str, Any]
    result: Dict[str, Any]

class ChatResponse(BaseModel):
    conversation_id: int
    message_id: int
    response: str
    tool_calls: List[ToolCall] = []
```

### 2. Chat Route

**File:** `backend/app/routes/chat.py`

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List, Dict, Any

from app.schemas.chat import ChatRequest, ChatResponse
from app.db.database import get_db
from app.db.queries import chat as chat_queries
from app.ai.openai_client import chat_with_ai, execute_function, get_final_response
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/api", tags=["chat"])

@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat(
    user_id: str,
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Main chat endpoint - handles user messages and AI responses.
    
    Flow:
    1. Get or create conversation
    2. Fetch message history
    3. Send to OpenAI
    4. Execute any function calls
    5. Get final AI response
    6. Store messages
    7. Return response
    """
    
    try:
        # Verify user
        if current_user["user_id"] != user_id:
            raise HTTPException(403, "Forbidden")
        
        # Step 1: Get or create conversation
        if request.conversation_id:
            conversation = chat_queries.get_conversation(
                db, request.conversation_id
            )
            if not conversation or conversation.user_id != user_id:
                raise HTTPException(404, "Conversation not found")
        else:
            conversation = chat_queries.create_conversation(db, user_id)
        
        # Step 2: Fetch conversation history (last 10 messages)
        history = chat_queries.get_conversation_history(
            db, conversation.id, limit=10
        )
        
        # Format history for OpenAI
        messages = [
            {"role": msg.role, "content": msg.content}
            for msg in history
        ]
        
        # Add new user message
        messages.append({"role": "user", "content": request.message})
        
        # Step 3: Send to OpenAI
        ai_response = chat_with_ai(messages, user_id)
        
        # Step 4: Execute function calls (if any)
        tool_calls = []
        if ai_response.get("requires_function_execution"):
            function_results = []
            
            for tool_call in ai_response["tool_calls"]:
                result = execute_function(
                    function_name=tool_call["function"],
                    arguments=tool_call["arguments"],
                    user_id=user_id,
                    db=db
                )
                
                function_results.append({
                    "tool_call_id": tool_call["id"],
                    **result
                })
                
                tool_calls.append({
                    "function": tool_call["function"],
                    "arguments": tool_call["arguments"],
                    "result": result
                })
            
            # Step 5: Get final response from AI
            final_response = get_final_response(messages, function_results)
        else:
            # No functions called, use direct response
            final_response = ai_response["content"]
        
        # Step 6: Store messages in database
        # Store user message
        user_msg = chat_queries.add_message(
            db=db,
            conversation_id=conversation.id,
            user_id=user_id,
            role="user",
            content=request.message
        )
        
        # Store AI response
        ai_msg = chat_queries.add_message(
            db=db,
            conversation_id=conversation.id,
            user_id=user_id,
            role="assistant",
            content=final_response,
            tool_calls={"calls": tool_calls} if tool_calls else None
        )
        
        # Step 7: Return response
        return ChatResponse(
            conversation_id=conversation.id,
            message_id=ai_msg.id,
            response=final_response,
            tool_calls=tool_calls
        )
        
    except HTTPException:
        raise
    except Exception as e:
        # Log error
        print(f"Chat error: {str(e)}")
        
        # Return error response
        raise HTTPException(500, f"Chat failed: {str(e)}")
```

### 3. Database Query Functions

**File:** `backend/app/db/queries/chat.py`

```python
from sqlmodel import Session, select
from datetime import datetime
from typing import Optional, List, Dict, Any

from app.models.conversation import Conversation
from app.models.message import Message

def create_conversation(db: Session, user_id: str) -> Conversation:
    """Create a new conversation."""
    conversation = Conversation(user_id=user_id)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation

def get_conversation(db: Session, conversation_id: int) -> Optional[Conversation]:
    """Get conversation by ID."""
    return db.get(Conversation, conversation_id)

def get_conversation_history(
    db: Session,
    conversation_id: int,
    limit: int = 10
) -> List[Message]:
    """Get last N messages from conversation."""
    statement = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.desc())
        .limit(limit)
    )
    messages = db.exec(statement).all()
    return list(reversed(messages))  # Return in chronological order

def add_message(
    db: Session,
    conversation_id: int,
    user_id: str,
    role: str,
    content: str,
    tool_calls: Optional[Dict[str, Any]] = None
) -> Message:
    """Add a message to conversation."""
    message = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        role=role,
        content=content,
        tool_calls=tool_calls
    )
    db.add(message)
    
    # Update conversation timestamp
    conversation = db.get(Conversation, conversation_id)
    if conversation:
        conversation.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(message)
    return message

def get_user_conversations(
    db: Session,
    user_id: str,
    limit: int = 20
) -> List[Conversation]:
    """Get user's recent conversations."""
    statement = (
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.updated_at.desc())
        .limit(limit)
    )
    return db.exec(statement).all()
```

### 4. Register Route

**File:** `backend/app/main.py`

```python
from fastapi import FastAPI
from app.routes import chat

app = FastAPI()

# Register chat routes
app.include_router(chat.router)
```

## Stateless Design

### Key Principle
**Server holds NO state between requests.**

### How It Works

**Request 1:**
```python
# User: "Add buy groceries"
# Server:
1. No history (new conversation created)
2. conversation_id = 1
3. Process message
4. Store in DB
5. Return response
6. ✅ Forget everything (stateless)
```

**Request 2:**
```python
# User: "Show my tasks"
# Server:
1. Get conversation_id = 1
2. Fetch history from DB
3. Has context from database
4. Process message
5. Store in DB
6. Return response
7. ✅ Forget everything (stateless)
```

**Benefits:**
- Can restart server without losing state ✅
- Horizontal scaling (multiple servers) ✅
- Each request independent ✅
- Easy testing ✅

## Error Handling

### Common Errors

**1. Invalid Conversation ID:**
```python
if not conversation or conversation.user_id != user_id:
    raise HTTPException(404, "Conversation not found")
```

**2. Empty Message:**
```python
# Handled by Pydantic
message: str = Field(..., min_length=1)
```

**3. OpenAI Error:**
```python
try:
    ai_response = chat_with_ai(messages, user_id)
except Exception as e:
    raise HTTPException(500, f"AI error: {str(e)}")
```

**4. Function Execution Error:**
```python
result = execute_function(...)
if not result.get("success"):
    # AI will handle error in response
    pass
```

## Testing

### Manual Testing with curl

**Test 1: New Conversation**
```bash
curl -X POST http://localhost:8000/api/test@example.com/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Add buy milk"}'

# Should return conversation_id
```

**Test 2: Continue Conversation**
```bash
curl -X POST http://localhost:8000/api/test@example.com/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Show my tasks",
    "conversation_id": 1
  }'

# Should have context from previous message
```

**Test 3: Function Execution**
```bash
curl -X POST http://localhost:8000/api/test@example.com/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What do I need to do?",
    "conversation_id": 1
  }'

# Should call list_tasks function
```

### Automated Tests

**File:** `backend/tests/test_chat_api.py`

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_new_conversation():
    response = client.post(
        "/api/test@example.com/chat",
        json={"message": "Hello"}
    )
    assert response.status_code == 200
    assert "conversation_id" in response.json()

def test_continue_conversation():
    # First message
    resp1 = client.post(
        "/api/test@example.com/chat",
        json={"message": "Add task 1"}
    )
    conv_id = resp1.json()["conversation_id"]
    
    # Second message
    resp2 = client.post(
        "/api/test@example.com/chat",
        json={
            "message": "Show my tasks",
            "conversation_id": conv_id
        }
    )
    assert resp2.status_code == 200
    assert "task 1" in resp2.json()["response"].lower()
```

## Performance Considerations

### Response Time

**Target:** < 2 seconds per request

**Breakdown:**
- DB query (history): ~20ms
- OpenAI API call: ~1000ms
- Function execution: ~50ms
- DB write (messages): ~30ms
- **Total: ~1.1s** ✅

### Optimizations

1. **Limit History:**
```python
# Only last 10 messages
limit=10
```

2. **Database Indexes:**
```sql
INDEX idx_conversation_id ON messages(conversation_id)
```

3. **Async Operations:**
```python
async def chat(...):
    # FastAPI handles async
```

## Success Criteria

- [ ] Endpoint accepts POST requests
- [ ] Creates new conversations
- [ ] Fetches conversation history
- [ ] Integrates with OpenAI
- [ ] Executes functions correctly
- [ ] Stores messages in database
- [ ] Returns proper responses
- [ ] Handles errors gracefully
- [ ] Stateless design verified
- [ ] Response time < 2s

---

**Estimated Time:** 3-4 hours with Qwen
**Priority:** High - Core backend feature
**Dependencies:** Database schema, OpenAI integration
