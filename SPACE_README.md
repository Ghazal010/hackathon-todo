---
title: DreamFlow AI Todo Backend
emoji: 🚀
colorFrom: purple
colorTo: blue
sdk: docker
pinned: false
license: mit
---

# DreamFlow AI Todo Backend API

A FastAPI backend for the DreamFlow AI-powered todo application with authentication and OpenAI integration.

## Overview
This is the backend API for a full-stack AI-powered todo application featuring:
- User authentication (register/login)
- Task management with priorities, categories, tags
- Natural language processing with OpenAI
- Chat interface for task management
- Database integration with PostgreSQL

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