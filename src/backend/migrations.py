"""
Database migration script to add user_id column to tasks table
"""

import sqlite3
import sys
from pathlib import Path

def migrate_database():
    """Add user_id column to tasks table"""
    # Get the database path from the existing database file
    db_path = Path("./todo_app.db")

    if not db_path.exists():
        print(f"Database not found at {db_path}")
        return False

    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()

        # Check if user_id column already exists
        cursor.execute("PRAGMA table_info(tasks)")
        columns = [column[1] for column in cursor.fetchall()]

        if 'user_id' in columns:
            print("user_id column already exists")
            conn.close()
            return True

        # Add user_id column to tasks table
        cursor.execute("""
            ALTER TABLE tasks
            ADD COLUMN user_id TEXT DEFAULT 'default_user' NOT NULL
        """)

        # Create indexes for conversations and messages tables if they don't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER NOT NULL,
                user_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                tool_calls TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
            )
        """)

        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON conversations(user_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_messages_conversation_id ON messages(conversation_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_messages_user_id ON messages(user_id)")

        conn.commit()
        conn.close()

        print("Database migration completed successfully!")
        print("- Added user_id column to tasks table")
        print("- Created conversations table")
        print("- Created messages table")
        print("- Created necessary indexes")

        return True

    except Exception as e:
        print(f"Migration failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = migrate_database()
    sys.exit(0 if success else 1)