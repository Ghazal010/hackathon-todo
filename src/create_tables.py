#!/usr/bin/env python3
"""
Script to create database tables
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.backend.database import create_tables

if __name__ == "__main__":
    print("Creating database tables...")
    create_tables()
    print("Tables created successfully!")

    # Now run the migration
    from src.backend.migrations import migrate_database
    migrate_database()
    print("Migration completed!")