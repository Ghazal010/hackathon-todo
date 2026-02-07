---
title: DreamFlow AI Todo App
emoji: 🚀
colorFrom: purple
colorTo: blue
sdk: docker
pinned: false
license: mit
---

# DreamFlow AI Todo App

A full-stack AI-powered todo application with authentication and natural language processing.

## Overview
This is a full-stack AI-powered todo application featuring:
- User authentication system (register/login)
- Natural language task management with AI
- Beautiful UI with dark/light mode
- Task categorization and prioritization
- Progress tracking and subtasks
- AI chatbot for task management

## Usage
The application is deployed as a Docker container on Hugging Face Spaces. It serves as the backend API for the todo application.

### API Endpoints
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

### Environment Variables
- `OPENAI_API_KEY` - Your OpenAI API key (required)
- `DATABASE_URL` - Database connection string (auto-provisioned)

## Environment Variables Required
- `OPENAI_API_KEY`: Your OpenAI API key for AI features