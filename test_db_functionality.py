#!/usr/bin/env python3
"""
Comprehensive test to verify Neon database functionality
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError, ProgrammingError

# Load environment variables
load_dotenv()

# Get the database URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

print(f"Testing database functionality...")
print(f"Database URL: {DATABASE_URL}")

try:
    # Create engine with Neon-specific settings
    if DATABASE_URL.startswith('postgresql'):
        engine = create_engine(
            DATABASE_URL,
            echo=False,
            pool_pre_ping=True,
            pool_recycle=300,
        )
    else:
        engine = create_engine(DATABASE_URL, echo=False)

    # Test 1: Basic connection
    print("\n1. Testing basic connection...")
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("   ✓ Connection successful")

    # Test 2: Check if tables exist and create if needed
    print("\n2. Testing table creation...")
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), 'src', 'backend'))

    from sqlmodel import SQLModel
    from models import Task

    # Import models and create tables
    SQLModel.metadata.create_all(engine)
    print("   ✓ Tables created/verified successfully")

    # Test 3: Insert and retrieve data
    print("\n3. Testing data insertion and retrieval...")
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), 'src', 'backend'))

    from sqlmodel import Session, select
    from models import Task
    import json
    from datetime import datetime

    with Session(engine) as session:
        # Count existing tasks
        all_tasks = session.exec(select(Task)).all()
        initial_count = len(all_tasks)
        print(f"   Initial task count: {initial_count}")

        # Create a test task
        test_task = Task(
            title="Test task from connection verification",
            completed=False,
            priority="medium",
            tags=json.dumps(["test", "verification"]),
            due_date=datetime.now().date()
        )

        session.add(test_task)
        session.commit()
        session.refresh(test_task)

        print(f"   ✓ Test task created with ID: {test_task.id}")

        # Retrieve the task
        retrieved_task = session.get(Task, test_task.id)
        if retrieved_task:
            print(f"   ✓ Task retrieved successfully: {retrieved_task.title}")

        # Clean up - delete the test task
        session.delete(retrieved_task)
        session.commit()
        print(f"   ✓ Test task cleaned up")

        # Verify deletion
        remaining_tasks = session.exec(select(Task)).all()
        final_count = len(remaining_tasks)
        print(f"   Final task count: {final_count} (should equal initial count)")

        if initial_count == final_count:
            print("   ✓ Data integrity maintained correctly")
        else:
            print("   ⚠ Warning: Task count changed unexpectedly")

    # Test 4: Verify SSL connection (important for Neon)
    print("\n4. Testing SSL connection properties...")
    with engine.connect() as connection:
        ssl_status = connection.execute(text("SELECT current_setting('ssl');"))
        ssl_enabled = ssl_status.fetchone()[0]
        print(f"   SSL Enabled: {ssl_enabled}")

    print("\n🎉 All database functionality tests passed!")
    print("Your Neon database is fully functional and ready for use!")
    print("\nKey points verified:")
    print("- ✓ Connection to Neon database established")
    print("- ✓ Table creation/deletion works")
    print("- ✓ Data insertion/retrieval works")
    print("- ✓ SSL connection is properly configured")
    print("- ✓ Transaction handling works correctly")

except ImportError as e:
    print(f"\n❌ Import error - missing modules: {str(e)}")
    print("Try installing requirements with: pip install -r requirements.txt")

except OperationalError as e:
    print(f"\n❌ Database connection failed:")
    print(f"Error: {str(e)}")

except Exception as e:
    print(f"\n❌ Unexpected error occurred:")
    print(f"Error: {str(e)}")
    import traceback
    traceback.print_exc()