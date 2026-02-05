from sqlmodel import SQLModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from sqlalchemy import JSON


class ConversationBase(SQLModel):
    user_id: str


class Conversation(ConversationBase, table=True):
    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(max_length=255, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class MessageBase(SQLModel):
    conversation_id: int
    user_id: str
    role: str  # 'user' or 'assistant'
    content: str


class Message(MessageBase, table=True):
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    user_id: str = Field(max_length=255, index=True)
    role: str = Field(max_length=20)  # 'user' or 'assistant'
    content: str
    tool_calls: Optional[str] = Field(default=None)  # Store as JSON string
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)


class ChatRequest(SQLModel):
    message: str
    conversation_id: Optional[int] = None


class ToolCall(SQLModel):
    function: str
    arguments: Dict[str, Any]
    result: Dict[str, Any]


class ChatResponse(SQLModel):
    conversation_id: int
    message_id: int
    response: str
    tool_calls: list[ToolCall] = []


# Import existing models for reference in the chat system
__all__ = [
    "Conversation",
    "Message",
    "ChatRequest",
    "ChatResponse",
    "ToolCall"
]