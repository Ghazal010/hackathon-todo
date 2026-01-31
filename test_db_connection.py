#!/usr/bin/env python3
"""
Test script to verify Neon database connection
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError, ProgrammingError

# Load environment variables
load_dotenv()

# Get the database URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

print(f"Testing database connection...")
print(f"Database URL: {DATABASE_URL}")

try:
    # Create engine
    if DATABASE_URL.startswith('postgresql'):
        # PostgreSQL settings for Neon
        engine = create_engine(
            DATABASE_URL,
            echo=False,  # Set to True for SQL debugging
            pool_pre_ping=True,  # Verify connections before use
            pool_recycle=300,    # Recycle connections after 5 minutes
        )
    else:
        # SQLite settings
        engine = create_engine(DATABASE_URL, echo=False)

    # Test the connection
    print("\nAttempting to connect to the database...")
    with engine.connect() as connection:
        # Execute a simple query
        result = connection.execute(text("SELECT 1"))
        print("✓ Database connection successful!")

        # If PostgreSQL, get version info
        if DATABASE_URL.startswith('postgresql'):
            version_result = connection.execute(text("SELECT version();"))
            version = version_result.fetchone()[0]
            print(f"PostgreSQL version: {version[:50]}...")

        print(f"✓ Successfully executed test query")

    print("\n🎉 Database connection test passed!")
    print("Your Neon database is properly configured and accessible.")

except OperationalError as e:
    print(f"\n❌ Database connection failed:")
    print(f"Error: {str(e)}")
    print("\nThis could be due to:")
    print("- Incorrect connection string in .env file")
    print("- Network/firewall issues")
    print("- Invalid credentials")
    print("- Database server not running")

except Exception as e:
    print(f"\n❌ Unexpected error occurred:")
    print(f"Error: {str(e)}")

print(f"\nNote: Current DATABASE_URL is {'PostgreSQL (Neon)' if DATABASE_URL.startswith('postgresql') else 'SQLite'}")