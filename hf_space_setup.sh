#!/bin/bash

# Script to prepare your existing backend for Hugging Face Spaces deployment

echo "Setting up Hugging Face Space for DreamFlow backend..."

# Clone the Hugging Face Space repository
echo "Cloning your Hugging Face Space repository..."
git clone https://huggingface.co/spaces/ghazakshaikh1/To-do-app hf-space-temp

# Navigate to the space directory
cd hf-space-temp

# Remove the default files
rm -f app.py requirements.txt Dockerfile

# Copy the essential files from your existing project
cp -r /Users/user/Desktop/hackathon-todo/src ./src
cp /Users/user/Desktop/hackathon-todo/requirements.txt ./
cp /Users/user/Desktop/hackathon-todo/Dockerfile ./

# Create a simple entrypoint for Hugging Face
cat > app.py << 'EOF'
from src.backend.main import app

# This simply imports your existing FastAPI app
# Hugging Face Spaces will run this with uvicorn automatically
if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 7860))  # Hugging Face uses port 7860
    uvicorn.run(app, host="0.0.0.0", port=port)
EOF

# Update the Dockerfile to work with Hugging Face's requirements
cat > Dockerfile << 'EOF'
# Use Python 3.13 slim image
FROM python:3.13-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose port required by Hugging Face Spaces
EXPOSE 7860

# Run the application
CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
EOF

# Create/update the README for Hugging Face Spaces
cat > README.md << 'EOF'
---
title: DreamFlow AI Todo Backend
emoji: 🚀
colorFrom: purple
colorTo: blue
sdk: docker
pinned: false
license: mit
---

# DreamFlow AI Todo Backend

A full-stack AI-powered todo application with authentication and natural language processing.

## Overview
This is the backend API for a full-stack AI-powered todo application featuring:
- User authentication system (register/login)
- Natural language task management with AI
- Beautiful UI with dark/light mode
- Task categorization and prioritization
- Progress tracking and subtasks
- AI chatbot for task management

## API Endpoints
- `POST /api/register` - User registration
- `POST /api/login` - User login
- `GET /api/users/me` - Get current user
- `GET /api/tasks` - Get user's tasks
- `POST /api/tasks` - Create a new task
- `PUT /api/tasks/{task_id}` - Update a task
- `DELETE /api/tasks/{task_id}` - Delete a task
- `PATCH /api/tasks/{task_id}/toggle-complete` - Toggle task completion
- `GET /api/tasks/stats` - Get task statistics
- `POST /api/chat` - AI chat interface

## Environment Variables Required
- `OPENAI_API_KEY`: Your OpenAI API key for AI features
EOF

# Add the updated files to git
git add .
git config --global user.email "user@example.com"
git config --global user.name "User"
git commit -m "Update with DreamFlow backend application"
git push

echo "Setup complete! Your Hugging Face Space should now be updated with your backend."
echo "Remember to add your OPENAI_API_KEY as a secret in your Space settings."