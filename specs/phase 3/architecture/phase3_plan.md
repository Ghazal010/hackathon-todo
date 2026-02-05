# Phase 3: AI-Powered Todo Chatbot

## Overview
Transform the todo app into an AI-powered chatbot that manages tasks through natural language conversations using Google Gemini.

## Objective
Users can manage their tasks by chatting naturally - "Add buy groceries", "Show my tasks", "Mark task 3 as done" - instead of clicking buttons.

## Timeline
- **Due Date**: December 21, 2025
- **Points**: 200
- **Status**: 🚧 Planning

## Key Changes from Phase 2

### What's New
- ✨ **Chat Interface**: Replace button-based UI with conversational interface
- 🤖 **AI Understanding**: Gemini interprets natural language
- 💾 **Conversation History**: Store chat messages in database
- 🔧 **Function Calling**: Gemini calls task functions automatically
- 📊 **Stateless Design**: Server doesn't hold conversation state

### What Stays Same
- ✅ Task CRUD operations (same backend functions)
- ✅ Database (just add conversations/messages tables)
- ✅ Authentication (Better Auth)
- ✅ Task data model

## Technology Stack

### AI & Chat
- **AI Engine**: OpenAI GPT-4o-mini (budget-friendly)
- **Function Calling**: OpenAI function calling (tools)
- **Chat UI**: Custom React component (simple, no ChatKit needed)

### Backend
- **Framework**: Python FastAPI (same as Phase 2)
- **ORM**: SQLModel
- **Database**: Neon PostgreSQL
- **New Endpoint**: POST /api/{user_id}/chat

### Frontend
- **Framework**: Next.js 16+ (same as Phase 2)
- **UI**: Custom chat interface with your purple theme
- **Real-time**: Optional WebSocket for live updates

## Architecture

```
User Types Message
       ↓
   Chat UI (Frontend)
       ↓
   POST /api/chat
       ↓
FastAPI Backend receives message
       ↓
Fetch conversation history from DB
       ↓
Send to Gemini with:
  - User message
  - Conversation history
  - Available functions
       ↓
Gemini decides which function to call
       ↓
Execute function (add_task, list_tasks, etc.)
       ↓
Get result from database
       ↓
Send result back to Gemini
       ↓
Gemini generates friendly response
       ↓
Save message & response to DB
       ↓
Return response to frontend
       ↓
Display in chat UI
```

## Features to Implement

### 1. Chat API Endpoint ✅
**Spec**: `specs/phase3/features/chat-api.md`

**Functionality:**
- Accept user message
- Fetch conversation history
- Process with Gemini
- Execute tool calls
- Store messages
- Return AI response

**Endpoint:**
```
POST /api/{user_id}/chat
Body: { "message": "Add buy groceries", "conversation_id": 123 }
Response: { "response": "Task added!", "conversation_id": 123 }
```

### 2. Gemini Integration ✅
**Spec**: `specs/phase3/features/gemini-integration.md`

**Features:**
- Function calling setup
- Tool definitions for all 5 task operations
- Conversation management
- Error handling

**Tools to Define:**
1. `add_task(title, description)`
2. `list_tasks(status)` 
3. `complete_task(task_id)`
4. `update_task(task_id, title, description)`
5. `delete_task(task_id)`

### 3. Chat UI Component ✅
**Spec**: `specs/phase3/features/chat-ui.md`

**Features:**
- Message list with scrolling
- User vs AI message bubbles
- Input field with send button
- Loading states ("AI is typing...")
- Error handling
- Conversation persistence

### 4. Database Schema ✅
**Spec**: `specs/phase3/features/database-schema.md`

**New Tables:**
- `conversations` - Chat sessions
- `messages` - Individual messages

**Updates:**
- None needed for `tasks` table

### 5. Conversation State Management ✅
**Spec**: `specs/phase3/features/conversation-state.md`

**Features:**
- Create new conversation
- Resume existing conversation
- Fetch message history
- Stateless server design

## Implementation Order

### Week 1: Backend (Days 1-3)

**Day 1: Database & Models**
- [ ] Create conversations table
- [ ] Create messages table
- [ ] Update SQLModel models
- [ ] Migration scripts

**Day 2: Gemini Setup**
- [ ] Get Gemini API key
- [ ] Install google-generativeai package
- [ ] Define function schemas
- [ ] Test function calling

**Day 3: Chat API**
- [ ] Create /api/chat endpoint
- [ ] Implement conversation fetching
- [ ] Integrate Gemini
- [ ] Handle function execution
- [ ] Store messages

### Week 2: Frontend (Days 4-7)

**Day 4: Chat UI Component**
- [ ] Create ChatInterface component
- [ ] Message bubbles (user/AI)
- [ ] Input field
- [ ] Send button

**Day 5: Integration**
- [ ] Connect UI to API
- [ ] Handle responses
- [ ] Display messages
- [ ] Error handling

**Day 6: Polish**
- [ ] Loading states
- [ ] Scroll to bottom
- [ ] Timestamps
- [ ] Empty states

**Day 7: Testing & Demo**
- [ ] Test all commands
- [ ] Record demo video
- [ ] Push to GitHub
- [ ] Submit

## Natural Language Commands

The AI should understand these types of commands:

### Task Creation
- "Add buy groceries"
- "Create a task to call mom"
- "Remember to pay bills"
- "New task: finish report"

### Task Listing
- "Show my tasks"
- "What do I need to do?"
- "List all tasks"
- "What's pending?"
- "Show completed tasks"

### Task Completion
- "Mark task 3 as done"
- "Complete the groceries task"
- "Task 1 is finished"

### Task Update
- "Change task 2 to 'Call mom tonight'"
- "Update the title of task 5"
- "Rename task 3"

### Task Deletion
- "Delete task 4"
- "Remove the meeting task"
- "Cancel task 1"

### Conversational
- "Hi" / "Hello" → Friendly greeting
- "Help" → Show available commands
- "Thanks" → You're welcome response

## API Specifications

### Chat Endpoint

**Request:**
```json
POST /api/{user_id}/chat

{
  "message": "Add buy groceries",
  "conversation_id": 123  // Optional, creates new if not provided
}
```

**Response:**
```json
{
  "conversation_id": 123,
  "response": "✅ Task added successfully! \n\n[1] ⬜ Buy groceries\n    Created just now",
  "tool_calls": [
    {
      "function": "add_task",
      "arguments": {"title": "Buy groceries"},
      "result": {"task_id": 1, "title": "Buy groceries"}
    }
  ]
}
```

### Function Schemas for Gemini

```python
tools = [
    {
        "name": "add_task",
        "description": "Create a new task",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Task title"},
                "description": {"type": "string", "description": "Task description"}
            },
            "required": ["title"]
        }
    },
    {
        "name": "list_tasks",
        "description": "Get list of tasks",
        "parameters": {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string", 
                    "enum": ["all", "pending", "completed"],
                    "description": "Filter by status"
                }
            }
        }
    },
    # ... other tools
]
```

## UI Component Structure

```
frontend/
├── components/
│   ├── chat/
│   │   ├── ChatInterface.tsx      # Main chat component
│   │   ├── MessageBubble.tsx      # Single message
│   │   ├── MessageList.tsx        # Scrollable list
│   │   ├── ChatInput.tsx          # Input + send button
│   │   └── TypingIndicator.tsx    # "AI is typing..."
│   └── ui/
│       └── ... (shadcn components)
└── app/
    └── chat/
        └── page.tsx               # Chat page
```

## Stateless Server Design

**Key Principle:** Server holds NO state between requests

### How It Works:

**Request 1:**
```
User: "Add buy groceries"
Server: 
  1. No history (new conversation)
  2. Create conversation in DB
  3. Call Gemini
  4. Execute add_task
  5. Store user message + AI response
  6. Return response
  7. FORGET EVERYTHING ✅
```

**Request 2:**
```
User: "Show my tasks"
Server:
  1. Fetch conversation history from DB
  2. Send history + new message to Gemini
  3. Gemini has context from DB
  4. Execute list_tasks
  5. Store new messages
  6. Return response
  7. FORGET EVERYTHING ✅
```

**Benefits:**
- Can restart server without losing state
- Can scale horizontally (multiple servers)
- Each request independent
- Easy to test

## Testing Strategy

### Manual Test Cases

**Test 1: First Message**
1. Open chat
2. Type: "Add buy groceries"
3. ✅ Task created
4. ✅ Friendly response
5. ✅ Message saved to DB

**Test 2: Conversation Context**
1. Add task: "Buy groceries"
2. Then say: "Mark it as done"
3. ✅ AI understands "it" = last task
4. ✅ Task marked complete

**Test 3: Multiple Commands**
1. "Add task 1, task 2, and task 3"
2. ✅ All 3 tasks created
3. ✅ Confirmation for each

**Test 4: Error Handling**
1. "Mark task 999 as done"
2. ✅ AI responds: "Task 999 not found"

**Test 5: Resume Conversation**
1. Create tasks
2. Refresh page
3. Send new message
4. ✅ AI remembers context

## Quality Checklist

### Backend
- [ ] Chat endpoint working
- [ ] Gemini integration complete
- [ ] All 5 tool functions working
- [ ] Conversation stored in DB
- [ ] Stateless design verified
- [ ] Error handling robust

### Frontend
- [ ] Chat UI displays correctly
- [ ] Messages scroll properly
- [ ] Input/send working
- [ ] Loading states shown
- [ ] Error messages displayed
- [ ] Conversation persists

### AI Behavior
- [ ] Understands all command types
- [ ] Calls correct functions
- [ ] Provides helpful responses
- [ ] Handles errors gracefully
- [ ] Maintains conversation context

## Environment Variables

### Backend (.env)
```bash
# Gemini API
GEMINI_API_KEY=your_gemini_api_key

# Database (same as Phase 2)
DATABASE_URL=postgresql://...

# Auth (same as Phase 2)
BETTER_AUTH_SECRET=...
```

### Frontend (.env.local)
```bash
# API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Auth
NEXT_PUBLIC_BETTER_AUTH_URL=...
```

## Success Criteria

Phase 3 complete when:
1. ✅ User can chat with AI
2. ✅ AI performs all 5 task operations
3. ✅ Conversation persists in database
4. ✅ Server is stateless
5. ✅ UI is clean and functional
6. ✅ Demo video shows natural language commands

## Resources

### Gemini
- Docs: https://ai.google.dev/docs
- Function Calling: https://ai.google.dev/docs/function_calling
- Python SDK: https://pypi.org/project/google-generativeai/

### FastAPI
- Docs: https://fastapi.tiangolo.com/

### Next.js
- Docs: https://nextjs.org/docs

## Next Phase Preview

**Phase 4:** Deploy on Kubernetes
- Docker containers
- Minikube locally
- Helm charts
- kubectl-ai

---

**Let's build the AI chatbot! 🤖✨**
