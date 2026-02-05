from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timedelta
from sqlalchemy import JSON
import bcrypt
import jwt
from enum import Enum

# Secret key for JWT encoding/decoding - should be in environment variables
SECRET_KEY = "your-secret-key-change-this-in-production"  # Change this in production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Priority(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"

class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False, max_length=255)
    username: str = Field(unique=True, nullable=False, max_length=255)

class User(UserBase, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, nullable=False, max_length=255)
    username: str = Field(unique=True, nullable=False, max_length=255)
    hashed_password: str = Field(nullable=False, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(UserBase):
    password: str

class UserRegister(SQLModel):
    email: str
    username: str
    password: str

class UserLogin(SQLModel):
    email: str
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime

class Token(SQLModel):
    access_token: str
    token_type: str

class TokenData(SQLModel):
    username: Optional[str] = None

class TaskBase(SQLModel):
    title: str
    completed: bool = False
    priority: str = "medium"  # "high", "medium", "low"
    tags: Optional[str] = "[]"  # Store as JSON string
    due_date: Optional[str] = None  # ISO date format

class Task(TaskBase, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(nullable=False, foreign_key="users.id", index=True)  # Reference to users table
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TaskCreate(TaskBase):
    pass  # Same as base but without ID

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    tags: Optional[str] = None
    due_date: Optional[str] = None

class TaskResponse(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime