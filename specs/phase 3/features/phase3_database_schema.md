# Feature: Database Schema for Chat

## Overview
Add two new tables to support conversational AI: `conversations` and `messages`. The `tasks` table remains unchanged.

## User Story
As a system, I need to store chat conversations and messages so that users can have continuous conversations with the AI assistant across sessions.

## Database Tables

### Table 1: conversations

**Purpose:** Track individual chat sessions

```sql
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Indexes
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at)
);
```

**SQLModel Definition:**
```python
from sqlmodel import Field, SQLModel
from datetime import datetime
from typing import Optional

class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(max_length=255, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Table 2: messages

**Purpose:** Store individual messages in conversations

```sql
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,  -- 'user' or 'assistant'
    content TEXT NOT NULL,
    tool_calls JSONB,  -- Optional: store function calls
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE,
    
    -- Indexes
    INDEX idx_conversation_id (conversation_id),
    INDEX idx_created_at (created_at),
    INDEX idx_user_id (user_id)
);
```

**SQLModel Definition:**
```python
from sqlmodel import Field, SQLModel, Column
from sqlalchemy import JSON
from datetime import datetime
from typing import Optional, Dict, Any

class Message(SQLModel, table=True):
    __tablename__ = "messages"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    user_id: str = Field(max_length=255, index=True)
    role: str = Field(max_length=20)  # 'user' or 'assistant'
    content: str = Field(sa_column=Column("content", sqlalchemy.Text))
    tool_calls: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
```

### Table 3: tasks (Existing - No Changes)

**No modifications needed.** Same structure from Phase 2:

```python
class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(max_length=255, index=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default="", max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

## Data Relationships

```
User
  │
  ├─── Conversations (1 user → many conversations)
  │      │
  │      └─── Messages (1 conversation → many messages)
  │
  └─── Tasks (1 user → many tasks)
```

## Example Data Flow

### Creating a Conversation

**Scenario:** User opens chat for first time

```python
# 1. Create conversation
conversation = Conversation(user_id="ghazal@example.com")
db.add(conversation)
db.commit()
# conversation.id = 1

# 2. Store first message
message = Message(
    conversation_id=1,
    user_id="ghazal@example.com",
    role="user",
    content="Add buy groceries to my list"
)
db.add(message)
db.commit()

# 3. AI processes and responds
# 4. Store AI response
assistant_message = Message(
    conversation_id=1,
    user_id="ghazal@example.com",
    role="assistant",
    content="✅ Task added successfully! [1] ⬜ Buy groceries",
    tool_calls={"function": "add_task", "arguments": {"title": "Buy groceries"}}
)
db.add(assistant_message)
db.commit()
```

### Fetching Conversation History

**Scenario:** User returns to chat

```python
# Get last 10 messages from conversation
messages = db.query(Message)\
    .filter(Message.conversation_id == 1)\
    .order_by(Message.created_at.desc())\
    .limit(10)\
    .all()

# Reverse to chronological order
messages = list(reversed(messages))

# Format for OpenAI
openai_messages = [
    {"role": msg.role, "content": msg.content}
    for msg in messages
]
```

## Migration Script

**File:** `backend/alembic/versions/003_add_chat_tables.py`

```python
"""Add conversations and messages tables

Revision ID: 003
Revises: 002
Create Date: 2025-01-17
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

revision = '003'
down_revision = '002'

def upgrade():
    # Create conversations table
    op.create_table(
        'conversations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_conversations_user_id', 'conversations', ['user_id'])
    op.create_index('idx_conversations_created_at', 'conversations', ['created_at'])
    
    # Create messages table
    op.create_table(
        'messages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('conversation_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(length=255), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('tool_calls', JSONB, nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_messages_conversation_id', 'messages', ['conversation_id'])
    op.create_index('idx_messages_user_id', 'messages', ['user_id'])
    op.create_index('idx_messages_created_at', 'messages', ['created_at'])

def downgrade():
    op.drop_table('messages')
    op.drop_table('conversations')
```

## Database Queries

### Common Operations

**1. Create New Conversation:**
```python
def create_conversation(user_id: str) -> Conversation:
    conversation = Conversation(user_id=user_id)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation
```

**2. Get User's Conversations:**
```python
def get_user_conversations(user_id: str, limit: int = 10):
    return db.query(Conversation)\
        .filter(Conversation.user_id == user_id)\
        .order_by(Conversation.updated_at.desc())\
        .limit(limit)\
        .all()
```

**3. Add Message:**
```python
def add_message(
    conversation_id: int,
    user_id: str,
    role: str,
    content: str,
    tool_calls: dict = None
) -> Message:
    message = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        role=role,
        content=content,
        tool_calls=tool_calls
    )
    db.add(message)
    
    # Update conversation timestamp
    conversation = db.query(Conversation).get(conversation_id)
    conversation.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(message)
    return message
```

**4. Get Conversation History:**
```python
def get_conversation_history(
    conversation_id: int,
    limit: int = 10
) -> list[Message]:
    messages = db.query(Message)\
        .filter(Message.conversation_id == conversation_id)\
        .order_by(Message.created_at.desc())\
        .limit(limit)\
        .all()
    return list(reversed(messages))
```

**5. Delete Old Conversations (Cleanup):**
```python
from datetime import timedelta

def delete_old_conversations(days: int = 30):
    cutoff = datetime.utcnow() - timedelta(days=days)
    db.query(Conversation)\
        .filter(Conversation.updated_at < cutoff)\
        .delete()
    db.commit()
```

## Storage Considerations

### Conversation Limits

**Per User:**
- Max conversations: Unlimited (but cleanup old ones)
- Max messages per conversation: 1000 (soft limit)
- Message retention: 30 days (configurable)

**Per Message:**
- Content max length: 10,000 characters (TEXT type)
- Tool calls: Stored as JSONB (efficient)

### Neon Free Tier Limits

- Storage: 512 MB
- Rows: Unlimited
- Connections: 100 concurrent

**Estimated Storage:**
```
1 conversation ≈ 100 bytes
1 message ≈ 500 bytes (average)
1000 users × 10 conversations × 50 messages = 250 MB
✅ Well within free tier
```

## Indexes Strategy

**Why These Indexes:**

1. `idx_user_id` (conversations) - Fast user lookup
2. `idx_conversation_id` (messages) - Fast message fetching
3. `idx_created_at` - Sorting by time
4. Foreign key on conversation_id - Data integrity

**Performance:**
- Fetching 10 messages: ~5ms
- Creating message: ~2ms
- User conversations list: ~10ms

## Testing the Schema

### Test 1: Create and Query
```python
# Create
conv = Conversation(user_id="test@example.com")
db.add(conv)
db.commit()

msg = Message(
    conversation_id=conv.id,
    user_id="test@example.com",
    role="user",
    content="Hello"
)
db.add(msg)
db.commit()

# Query
messages = db.query(Message)\
    .filter(Message.conversation_id == conv.id)\
    .all()

assert len(messages) == 1
assert messages[0].content == "Hello"
```

### Test 2: Cascade Delete
```python
# Delete conversation
db.query(Conversation).filter(Conversation.id == conv.id).delete()
db.commit()

# Verify messages deleted too
messages = db.query(Message)\
    .filter(Message.conversation_id == conv.id)\
    .all()

assert len(messages) == 0  # Cascade delete worked
```

## Files to Create/Modify

### New Files:
```
backend/
├── app/
│   ├── models/
│   │   ├── conversation.py     # Conversation model
│   │   └── message.py          # Message model
│   └── db/
│       └── queries/
│           └── chat.py         # Chat-related queries
└── alembic/
    └── versions/
        └── 003_add_chat_tables.py
```

### Modified Files:
```
backend/
├── app/
│   └── db/
│       └── database.py         # Import new models
```

## Success Criteria

- [ ] Conversations table created in Neon
- [ ] Messages table created in Neon
- [ ] Foreign key constraint working
- [ ] Indexes created
- [ ] SQLModel models defined
- [ ] Migration script runs successfully
- [ ] Can create conversation
- [ ] Can add messages
- [ ] Can query conversation history
- [ ] Cascade delete works

---

**Estimated Time:** 2-3 hours with Qwen
**Priority:** High - Do this first
