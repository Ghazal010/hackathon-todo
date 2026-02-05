# Phase 3: Implementation Tasks

## Overview
Step-by-step task breakdown for Phase 3 AI Chatbot implementation. Each task is designed to be given to Qwen one at a time.

## Budget Reminder
- Model: GPT-4o-mini
- Budget: $5
- Expected spend: $2-3
- Monitor: https://platform.openai.com/usage

---

## 📋 TASK LIST

### TASK 0: Setup & Preparation
**Priority:** Do this FIRST
**Time:** 30 minutes

- [ ] 0.1 - Get OpenAI API key from https://platform.openai.com/api-keys
- [ ] 0.2 - Add $5 credit at https://platform.openai.com/account/billing
- [ ] 0.3 - Set hard limit to $5 at https://platform.openai.com/account/billing/limits
- [ ] 0.4 - Create `.env` file in backend with `OPENAI_API_KEY=sk-...`
- [ ] 0.5 - Install OpenAI SDK: `uv add openai` (in backend folder)
- [ ] 0.6 - Update PROJECT_STATUS.md to Phase 3
- [ ] 0.7 - Create specs/phase3/ folder structure

---

### TASK 1: Database Models
**Priority:** HIGH - Do Second
**Time:** 1-2 hours
**Spec:** `@specs/phase3/features/database-schema.md`
**Depends on:** Task 0

#### Give Qwen This:
```
Read @specs/phase3/features/database-schema.md

Create the following files:

1. backend/app/models/conversation.py
   - Conversation SQLModel class
   - Fields: id, user_id, created_at, updated_at

2. backend/app/models/message.py
   - Message SQLModel class
   - Fields: id, conversation_id, user_id, role, content, tool_calls, created_at
   - Foreign key to conversations table

3. Update backend/app/models/__init__.py
   - Import both new models

4. Create migration or update database setup
   - Add both tables to Neon database
```

#### Verify:
- [ ] Conversation model created
- [ ] Message model created
- [ ] Models imported correctly
- [ ] Tables created in Neon DB
- [ ] Foreign key working

---

### TASK 2: OpenAI Client Setup
**Priority:** HIGH
**Time:** 1-2 hours
**Spec:** `@specs/phase3/features/openai-integration.md`
**Depends on:** Task 0

#### Give Qwen This:
```
Read @specs/phase3/features/openai-integration.md

Create the following files:

1. backend/app/ai/__init__.py
   - Empty init file

2. backend/app/ai/tools.py
   - Define TOOLS list with all 5 functions:
     - add_task
     - list_tasks
     - complete_task
     - update_task
     - delete_task
   - Each tool has name, description, parameters

3. backend/app/ai/prompts.py
   - Define SYSTEM_PROMPT string
   - Keep it concise (under 150 tokens)
   - Friendly task assistant persona

4. backend/app/ai/openai_client.py
   - Initialize OpenAI client with API key from env
   - Use model: gpt-4o-mini
   - chat_with_ai() function
   - execute_function() function
   - get_final_response() function
   - Max tokens: 300
   - History limit: last 10 messages
```

#### Verify:
- [ ] Tools defined correctly (5 functions)
- [ ] System prompt is concise
- [ ] OpenAI client initializes
- [ ] chat_with_ai() works
- [ ] execute_function() handles all 5 operations
- [ ] Error handling in place

---

### TASK 3: Chat Database Queries
**Priority:** HIGH
**Time:** 1 hour
**Depends on:** Task 1

#### Give Qwen This:
```
Create backend/app/db/queries/chat.py with these functions:

1. create_conversation(db, user_id) → Conversation
   - Creates new conversation record

2. get_conversation(db, conversation_id) → Conversation | None
   - Gets conversation by ID

3. get_conversation_history(db, conversation_id, limit=10) → list[Message]
   - Gets last N messages
   - Returns in chronological order (oldest first)

4. add_message(db, conversation_id, user_id, role, content, tool_calls=None) → Message
   - Adds message to conversation
   - Updates conversation updated_at

5. get_user_conversations(db, user_id, limit=20) → list[Conversation]
   - Gets user's recent conversations
   - Ordered by updated_at desc

Use SQLModel Session for database operations.
Import models from app.models.conversation and app.models.message
```

#### Verify:
- [ ] All 5 query functions created
- [ ] create_conversation works
- [ ] get_conversation_history returns correct order
- [ ] add_message stores correctly
- [ ] No errors on import

---

### TASK 4: Chat API Endpoint
**Priority:** HIGH - Core Backend
**Time:** 2-3 hours
**Spec:** `@specs/phase3/features/chat-api.md`
**Depends on:** Task 1, 2, 3

#### Give Qwen This:
```
Read @specs/phase3/features/chat-api.md

Create/Update these files:

1. backend/app/schemas/chat.py
   - ChatRequest model (message: str, conversation_id: Optional[int])
   - ToolCall model
   - ChatResponse model (conversation_id, message_id, response, tool_calls)

2. backend/app/routes/chat.py
   - POST /api/{user_id}/chat endpoint
   - Flow:
     a. Get or create conversation
     b. Fetch history (last 10 messages)
     c. Send to OpenAI via chat_with_ai()
     d. If tool_calls: execute each function
     e. Get final response from OpenAI
     f. Store user message in DB
     g. Store AI response in DB
     h. Return ChatResponse

3. Update backend/app/main.py
   - Import and include chat router

Important:
- Use gpt-4o-mini model
- Limit history to 10 messages
- Set max_tokens=300
- Handle errors with HTTPException
- Stateless design (no in-memory state)
```

#### Verify:
- [ ] POST endpoint registered
- [ ] New conversation creates correctly
- [ ] Existing conversation continues
- [ ] OpenAI called with correct messages
- [ ] Functions execute correctly
- [ ] Messages stored in DB
- [ ] Response returned properly

#### Test with curl:
```bash
# Test new conversation
curl -X POST http://localhost:8000/api/test@email.com/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Add buy groceries"}'

# Test continue conversation (use returned conversation_id)
curl -X POST http://localhost:8000/api/test@email.com/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Show my tasks", "conversation_id": 1}'
```

---

### TASK 5: Chat History API
**Priority:** MEDIUM
**Time:** 30 minutes
**Depends on:** Task 3

#### Give Qwen This:
```
Add a new endpoint to backend/app/routes/chat.py:

GET /api/{user_id}/chat/history/{conversation_id}

Response:
{
  "conversation_id": 1,
  "messages": [
    {"id": 1, "role": "user", "content": "...", "created_at": "..."},
    {"id": 2, "role": "assistant", "content": "...", "created_at": "..."}
  ]
}

- Return last 50 messages
- Ordered chronologically (oldest first)
- Only return if conversation belongs to user
```

#### Verify:
- [ ] GET endpoint works
- [ ] Returns messages in order
- [ ] User ownership verified

---

### TASK 6: Chat UI Components
**Priority:** HIGH - Frontend
**Time:** 3-4 hours
**Spec:** `@specs/phase3/features/chat-ui.md`
**Depends on:** Task 4, 5

#### Give Qwen This:
```
Read @specs/phase3/features/chat-ui.md

Create these frontend components:

1. frontend/hooks/useChat.ts
   - Chat logic hook
   - State: messages, input, loading, error, conversationId
   - sendMessage() - calls POST /api/{user_id}/chat
   - loadHistory() - calls GET /api/{user_id}/chat/history/{id}
   - handleKeyPress() - Enter to send
   - newConversation() - reset chat
   - Auto-scroll ref

2. frontend/components/chat/ChatHeader.tsx
   - Dark purple header (#4A2040)
   - Logo + title "TaskFlow AI"
   - "New Chat" button

3. frontend/components/chat/MessageBubble.tsx
   - User messages: RIGHT side, purple (#C880B7), white text
   - AI messages: LEFT side, white background, pink border (#F5CCE8)
   - Timestamp below each message
   - Detect task patterns [ID] ☐/✅ and render as mini cards

4. frontend/components/chat/TypingIndicator.tsx
   - 3 bouncing purple dots
   - "AI is typing" text

5. frontend/components/chat/ChatInput.tsx
   - Text input with pink border (#EC9DED)
   - Round send button (#C880B7)
   - QuickActions below input

6. frontend/components/chat/QuickActions.tsx
   - 4 buttons: Show Tasks, Add Task, Completed, Pending
   - Light pink background (#F5CCE8)
   - Click fills input with preset text

7. frontend/components/chat/EmptyState.tsx
   - Welcome message when no messages
   - 4 suggestion cards with examples
   - Click suggestion to send

8. frontend/components/chat/ChatInterface.tsx
   - Main wrapper using useChat hook
   - Combines all components

9. frontend/app/chat/page.tsx
   - Page that renders ChatInterface

Colors to use:
- Header: #4A2040
- User bubble: #C880B7
- AI bubble: white with #F5CCE8 border
- Input border: #EC9DED
- Quick action bg: #F5CCE8
- Text headings: #4A2040
- Accent: #9F6BA0
```

#### Verify:
- [ ] Chat page renders
- [ ] Empty state shows first
- [ ] User message appears on right (purple)
- [ ] AI message appears on left (white/pink)
- [ ] Typing indicator shows while loading
- [ ] Quick actions fill input
- [ ] Suggestions on empty state work
- [ ] Timestamps display
- [ ] Mobile responsive

---

### TASK 7: Frontend-Backend Integration
**Priority:** HIGH
**Time:** 1-2 hours
**Depends on:** Task 4, 6

#### Give Qwen This:
```
Connect the frontend chat UI to the backend API:

1. Update frontend/lib/api.ts
   - Add chatMessage(message, conversationId) function
   - Add loadChatHistory(conversationId) function
   - Base URL from environment variable

2. Update frontend/hooks/useChat.ts
   - Use api.ts functions instead of direct fetch
   - Handle loading states properly
   - Handle errors properly
   - Save conversationId to localStorage

3. Add Next.js API proxy (optional but recommended)
   - frontend/app/api/chat/route.ts
   - Proxy requests to FastAPI backend
   - This avoids CORS issues

4. Create .env.local
   NEXT_PUBLIC_API_URL=http://localhost:8000

5. Test full flow:
   - Type message → Send → API call → AI response → Display
```

#### Verify:
- [ ] Message sends to backend
- [ ] Response displays in chat
- [ ] Conversation continues across messages
- [ ] Error handling works
- [ ] localStorage saves conversation ID
- [ ] Page refresh preserves conversation

---

### TASK 8: Testing All Features
**Priority:** HIGH - Do before submit
**Time:** 2 hours
**Depends on:** All tasks complete

#### Test Checklist:

**AI Commands:**
- [ ] "Add buy groceries" → Task created
- [ ] "Add call mom" with description → Task with description
- [ ] "Show me all my tasks" → Lists all tasks
- [ ] "What's pending?" → Shows incomplete tasks
- [ ] "Show completed tasks" → Shows done tasks
- [ ] "Mark task 1 as done" → Task completed
- [ ] "Mark task 1 as incomplete" → Task uncompleted
- [ ] "Update task 1 title to Buy fruits" → Title updated
- [ ] "Delete task 2" → Task removed
- [ ] "Help" → Shows available commands

**UI Tests:**
- [ ] Messages scroll correctly
- [ ] Typing indicator works
- [ ] Quick actions work
- [ ] Empty state shows correctly
- [ ] Mobile layout works
- [ ] Page refresh preserves chat

**Error Tests:**
- [ ] "Mark task 999 as done" → Error message
- [ ] "Delete task 999" → Error message
- [ ] Network error → Error displayed
- [ ] Empty message → Send disabled

**Cost Check:**
- [ ] Check https://platform.openai.com/usage
- [ ] Verify under $3 spent
- [ ] Under $5 hard limit

---

### TASK 9: Polish & Demo
**Priority:** Final step
**Time:** 1-2 hours
**Depends on:** Task 8 (all tests passing)

- [ ] 9.1 - Fix any bugs found in testing
- [ ] 9.2 - Update PROJECT_STATUS.md
- [ ] 9.3 - Update README.md with Phase 3 info
- [ ] 9.4 - Record demo video (90 seconds max)
- [ ] 9.5 - Git commit all changes
- [ ] 9.6 - Push to GitHub
- [ ] 9.7 - Submit on Google Form

#### Demo Video Script (90 seconds):
```
0:00 - 0:10 → Open app, show chat interface
0:10 - 0:20 → "Add buy groceries" → Show task created
0:20 - 0:30 → "Add call mom" → Show second task
0:30 - 0:40 → "Show me all my tasks" → Display both tasks
0:40 - 0:50 → "Mark task 1 as done" → Show completion
0:50 - 1:00 → "Update task 2" → Show update
1:00 - 1:10 → "Delete task 1" → Show deletion
1:10 - 1:20 → Show final task list
1:20 - 1:30 → End / Thank you screen
```

---

## 📊 TASK SUMMARY

| Task | Description | Time | Priority | Depends On |
|------|-------------|------|----------|------------|
| 0 | Setup & Prep | 30 min | FIRST | - |
| 1 | Database Models | 1-2 hrs | HIGH | 0 |
| 2 | OpenAI Client | 1-2 hrs | HIGH | 0 |
| 3 | Chat DB Queries | 1 hr | HIGH | 1 |
| 4 | Chat API Endpoint | 2-3 hrs | HIGH | 1,2,3 |
| 5 | Chat History API | 30 min | MED | 3 |
| 6 | Chat UI | 3-4 hrs | HIGH | 4,5 |
| 7 | Integration | 1-2 hrs | HIGH | 4,6 |
| 8 | Testing | 2 hrs | HIGH | All |
| 9 | Polish & Demo | 1-2 hrs | FINAL | 8 |

**Total Estimated Time:** 13-19 hours

---

## 🎯 HOW TO USE WITH QWEN

### Session Start:
```
Hi Qwen! Working on Phase 3 - AI Chatbot.
Read @PROJECT_STATUS.md for context.
```

### For Each Task:
```
Now working on TASK [N].
Read @specs/phase3/features/[spec-file].md
[Paste the "Give Qwen This" section from above]
```

### If Stuck:
```
Getting error: [error message]
Working on: [task number]
File: [filename]
Please help fix this.
```

### Session End:
```
Update @PROJECT_STATUS.md with:
- Tasks completed today
- Current task in progress
- Any issues encountered
- Next task to work on
```

---

## 💡 TIPS FOR SAVING TOKENS ($$$)

1. **One task at a time** - Don't give Qwen everything at once
2. **Be specific** - Clear instructions = less back and forth
3. **Test after each task** - Catch bugs early
4. **Use specs** - Reference spec files, don't repeat everything
5. **Update PROJECT_STATUS.md** - Saves context between sessions

---

## ✅ PHASE 3 COMPLETION CHECKLIST

### Backend
- [ ] Database models (conversations, messages)
- [ ] OpenAI integration (gpt-4o-mini)
- [ ] 5 tool functions defined
- [ ] Chat API endpoint working
- [ ] History API endpoint working
- [ ] Stateless design verified
- [ ] Error handling robust

### Frontend
- [ ] Chat UI renders correctly
- [ ] User/AI bubbles styled with purple theme
- [ ] Typing indicator works
- [ ] Quick actions work
- [ ] Empty state with suggestions
- [ ] Responsive design
- [ ] Connected to backend

### Testing
- [ ] All 5 task operations work via chat
- [ ] Conversation persists
- [ ] Error cases handled
- [ ] Mobile works
- [ ] Cost under $3

### Submission
- [ ] PROJECT_STATUS.md updated
- [ ] README.md updated
- [ ] Demo video recorded (90 sec)
- [ ] Code pushed to GitHub
- [ ] Form submitted

---

**Total Phase 3 Points: 200** 🎯
**Budget: $5 (expected spend: $2-3)** 💰
