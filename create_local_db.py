#!/usr/bin/env python3
"""
Script to create a local SQLite database for development
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from src.backend.database import create_tables
from dotenv import load_dotenv
import os

# Temporarily override the DATABASE_URL to use local SQLite
os.environ["DATABASE_URL"] = "sqlite:///./todo_app_local.db"

if __name__ == "__main__":
    print("Creating local database tables...")
    create_tables()
    print("Local tables created successfully!")
    print("Database file: ./todo_app_local.db")