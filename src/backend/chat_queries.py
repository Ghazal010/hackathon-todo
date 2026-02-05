from sqlmodel import Session, select
from typing import Optional, List
from datetime import datetime
from .chat_models import Conversation, Message


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
    tool_calls: Optional[dict] = None
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