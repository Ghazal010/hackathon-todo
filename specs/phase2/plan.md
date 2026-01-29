# Phase 2: Web Application with Elegant UI

## Overview
Transform the console todo app into a beautiful web application using the DreamFlow UI design with the specified purple pastel color scheme.

## Goals
- Implement the beautiful React UI with glass morphism effects
- Apply the specific color palette: Rose Mist, Lavender Dream, Orchid Whisper, Purple Haze, and Slate Purple
- Create a full-stack application with FastAPI backend
- Enable responsive design with dark/light mode
- Maintain all Phase 1 functionality with enhanced UI/UX

## Tech Stack
- Frontend: Next.js 16+ with Tailwind CSS
- Backend: Python FastAPI
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth with JWT
- Icons: Lucide React
- Fonts: Cormorant Garamond (headings), Quicksand (body)

## UI/UX Requirements

### Visual Design
- Implement glass morphism effect with backdrop-filter
- Use the exact color palette:
  - Rose Mist: #EAC8CA (accents)
  - Lavender Dream: #F2D5F8 (primary backgrounds)
  - Orchid Whisper: #E6C0E9 (gradients/highlights)
  - Purple Haze: #BFABCB (secondary elements)
  - Slate Purple: #8D89A6 (text/content)
- Apply gradient backgrounds (135deg: Lavender Dream → Orchid Whisper → Rose Mist)
- Include decorative animated blobs with blur effects

### Functional Requirements
- **Task Management**:
  - Add tasks with title, priority, tags, due date
  - View all tasks with filtering options
  - Update task details
  - Delete tasks
  - Mark tasks as complete/incomplete
  - Search functionality
  - Filter by: all, active, completed

- **Dashboard Elements**:
  - Stats cards showing Total, Completed, Active tasks
  - Priority indicators with color coding
  - Tag system with pill-shaped badges
  - Due date display with calendar icon

- **UI Interactions**:
  - Smooth animations (floating, slide-in, task-enter)
  - Hover lift effects
  - Ripple effects on buttons
  - Glass effect transitions
  - Dark/light mode toggle

### Responsive Design
- Mobile-first approach
- Responsive grid layouts
- Adaptive components for different screen sizes
- Touch-friendly interactions

## API Endpoints (REST)
- GET /api/tasks - Retrieve all tasks
- POST /api/tasks - Create new task
- PUT /api/tasks/{id} - Update task
- DELETE /api/tasks/{id} - Delete task
- PATCH /api/tasks/{id}/toggle-complete - Toggle completion status

### Task Object Structure
```json
{
  "id": "number",
  "title": "string",
  "completed": "boolean",
  "priority": "string (high|medium|low)",
  "tags": "string[]",
  "dueDate": "string (ISO date format)"
}
```

## Database Schema
- tasks table with columns: id, title, completed, priority, tags (JSON), due_date, created_at, updated_at

## Implementation Phases

### Phase 1: Backend Setup
- [ ] Set up FastAPI project
- [ ] Configure Neon PostgreSQL connection
- [ ] Create task model and database schema
- [ ] Implement CRUD API endpoints
- [ ] Add authentication with Better Auth

### Phase 2: Frontend Setup
- [ ] Create Next.js project
- [ ] Configure Tailwind CSS with custom colors
- [ ] Set up the exact UI from todo-app-ui.jsx
- [ ] Implement dark/light mode
- [ ] Add animations and glass morphism effects

### Phase 3: Integration
- [ ] Connect React UI to FastAPI backend
- [ ] Implement real-time task synchronization
- [ ] Add loading states and error handling
- [ ] Optimize performance

### Phase 4: Polish
- [ ] Responsive design adjustments
- [ ] Accessibility improvements
- [ ] Performance optimization
- [ ] Testing across devices

## Success Criteria
- [ ] All Phase 1 functionality preserved and enhanced
- [ ] Beautiful UI with exact color scheme implemented
- [ ] Responsive design works on mobile/desktop
- [ ] Dark/light mode functional
- [ ] All API endpoints working correctly
- [ ] Smooth animations and transitions
- [ ] Proper error handling and loading states
- [ ] Accessible and user-friendly interface

## Files to Create
- `src/backend/main.py` - FastAPI application
- `src/backend/models.py` - Database models
- `src/backend/database.py` - Database connection
- `src/backend/api.py` - API routes
- `src/frontend/pages/index.jsx` - Main UI page
- `src/frontend/components/*` - Reusable components
- `src/frontend/styles/*` - Custom styles
- `package.json` - Frontend dependencies
- `requirements.txt` - Backend dependencies