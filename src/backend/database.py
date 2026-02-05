from sqlmodel import create_engine, Session
from sqlalchemy import event
from urllib.parse import urlparse
import os
from dotenv import load_dotenv

load_dotenv()

# Get database URL from environment, default to SQLite for local development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

# For Neon, we need to handle SSL properly
def setup_ssl_verification(db_url: str):
    parsed = urlparse(db_url)
    if parsed.scheme == 'postgresql':
        # Add sslmode=require for Neon
        if '?sslmode=' not in db_url:
            db_url += "?sslmode=require"
    return db_url

if DATABASE_URL.startswith('postgresql'):
    DATABASE_URL = setup_ssl_verification(DATABASE_URL)

# Create engine with proper settings
# Use different settings for SQLite vs PostgreSQL
if DATABASE_URL.startswith('sqlite'):
    # SQLite settings
    engine = create_engine(
        DATABASE_URL,
        echo=False,  # Set to True for SQL debugging
    )
else:
    # PostgreSQL settings for Neon
    engine = create_engine(
        DATABASE_URL,
        echo=False,  # Set to True for SQL debugging
        pool_pre_ping=True,  # Verify connections before use
        pool_recycle=300,    # Recycle connections after 5 minutes
    )

def get_session():
    with Session(engine) as session:
        yield session

# Function to create tables
def create_tables():
    from .models import Task
    from .chat_models import Conversation, Message
    from sqlmodel import SQLModel

    SQLModel.metadata.create_all(engine)