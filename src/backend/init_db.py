#!/usr/bin/env python3
"""
Script to initialize the database with sample data
"""

from sqlmodel import Session, select
from database import create_tables, engine
from models import Task
from datetime import datetime
import json

def init_database():
    print("Creating tables...")
    create_tables()

    print("Adding sample data...")
    with Session(engine) as session:
        # Check if tasks already exist
        existing_tasks = session.exec(select(Task)).all()
        if existing_tasks:
            print("Database already has data, skipping initialization")
            return

        # Add sample tasks
        sample_tasks = [
            Task(
                title="Design new landing page",
                completed=False,
                priority="high",
                tags=json.dumps(["work"]),
                due_date="2024-02-15"
            ),
            Task(
                title="Morning meditation",
                completed=True,
                priority="medium",
                tags=json.dumps(["personal"]),
                due_date="2024-02-10"
            ),
            Task(
                title="Grocery shopping",
                completed=False,
                priority="low",
                tags=json.dumps(["errands"]),
                due_date="2024-02-12"
            )
        ]

        for task in sample_tasks:
            session.add(task)

        session.commit()
        print(f"Added {len(sample_tasks)} sample tasks to database")

if __name__ == "__main__":
    init_database()