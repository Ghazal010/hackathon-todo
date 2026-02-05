# Hackathon Todo App with OpenAI Integration & Authentication

A sophisticated full-stack AI-powered todo application featuring user authentication, natural language processing, beautiful UI, and advanced task management capabilities.

## 🎯 Project Goals
- Master Spec-Driven Development
- Build progressively complex software
- Learn cloud-native technologies
- Integrate OpenAI for enhanced productivity
- Create intuitive natural language task management

## 📅 Timeline

| Phase | Description | Due Date | Status |
|-------|-------------|----------|--------|
| I | Python Console App | Dec 7, 2025 | ✅ Complete |
| II | Full-Stack Web App | Dec 14, 2025 | ✅ Complete |
| III | AI Chatbot (OpenAI) | Dec 21, 2025 | ✅ Complete |
| IV | Local Kubernetes | Jan 4, 2026 | ⏳ Upcoming |
| V | Cloud Deployment | Jan 18, 2026 | ⏳ Upcoming |

## 🛠️ Tech Stack

### Backend
- Python 3.13+
- FastAPI for API framework
- SQLModel for database ORM
- PostgreSQL (via Neon) for database
- uvicorn for ASGI server

### Frontend
- Next.js 14 with App Router
- TypeScript support
- Tailwind CSS styling
- Lucide React icons
- Beautiful Purple-themed UI

### AI Integration
- OpenAI GPT-4o-mini for cost-effective processing
- Function calling for task operations
- Natural language processing for task management

## 🚀 Getting Started
```bash
# Clone repository
git clone https://github.com/Ghazal010/hackathon-todo.git
cd hackathon-todo

# Install dependencies
npm install  # For frontend

# Set up environment configuration
# Edit .env to add your OpenAI API key
OPENAI_API_KEY="your_openai_api_key_here"

# Start backend server (handles authentication and API)
cd src/backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000

# Start frontend server (includes login/signup)
cd frontend
npm run dev
# Visit http://localhost:3001 (or http://localhost:3000 if available)
# Register a new account or login to access the dashboard
```

## ⚡ OpenAI Configuration

The application is optimized for cost-effective API usage:

- **Model**: Uses `gpt-4o-mini` for optimal cost/performance
- **Token Limit**: Caps response tokens at 300 to control costs
- **Temperature**: Set to 0.7 for balanced creativity/consistency
- **Cost Control**: Designed to stay within reasonable usage limits

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | (required) |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-4o-mini` |
| `OPENAI_MAX_TOKENS` | Maximum tokens in response | `300` |
| `OPENAI_TEMPERATURE` | Creativity level (0.0-1.0) | `0.7` |

## 📋 Features

### Core Task Management
- ✅ Add Task
- ✅ Delete Task
- ✅ Update Task
- ✅ View Tasks
- ✅ Mark Complete
- ✅ Task Prioritization (High/Medium/Low)
- ✅ Category Management (Personal, Work, Health, etc.)
- ✅ Due Dates and Creation Tracking
- ✅ Tags System
- ✅ Recurring Tasks (Daily, Weekly, Monthly)
- ✅ Progress Tracking (Percentage Completion)
- ✅ Subtasks System
- ✅ Notification Reminders

### Advanced UI Features
- ✅ Beautiful UI with Purple Theme
- ✅ Dark/Light Mode Toggle
- ✅ Glass Morphism Effects
- ✅ Smooth Animations
- ✅ Responsive Design
- ✅ Search and Filtering
- ✅ Statistics Dashboard
- ✅ Advanced Task Management

### AI-Powered Features
- ✅ Natural Language Task Creation
- ✅ AI Chatbot for Task Management
- ✅ Function Calling for Backend Operations
- ✅ Conversational Task Management
- ✅ Smart Task Suggestions
- ✅ AI Task Enhancement: Get suggestions to improve your task titles and descriptions
- ✅ Natural Language Processing for intuitive interaction

## 🤖 AI Chat Interface

The application includes a sophisticated AI chat interface that allows natural language interaction:

1. **Conversational Task Management**: Simply say "Add buy groceries to my list" to create tasks
2. **Natural Language Processing**: AI understands context and intent
3. **Function Calling**: AI can directly interact with backend to perform CRUD operations
4. **Conversation History**: Maintains context across interactions
5. **Real-time Feedback**: Instant responses to user requests

### Available Commands
- "Add [task] to my list" - Creates new tasks
- "Show me my tasks" - Lists all tasks
- "Mark task [ID] as complete" - Updates task status
- "Delete task [ID]" - Removes tasks
- "Update task [ID] to [new details]" - Modifies tasks

## 🔐 Authentication System

The application now includes a complete user authentication system:

1. **User Registration**: Create new accounts with email and password
2. **Secure Login**: JWT-based authentication with password hashing
3. **Protected Routes**: All task data is user-specific and secured
4. **User Isolation**: Each user sees only their own tasks and data
5. **Session Management**: Automatic token handling and refresh

## 📖 Documentation
- `constitution.md` - Core principles
- `CLAUDE.md` - AI instructions
- `specs/` - Feature specifications
- `src/backend/` - Backend API implementation
- `src/backend/openai_client.py` - OpenAI integration
- `frontend/src/app/chat/` - AI Chat interface
- `WORK_SUMMARY.md` - Comprehensive work summary

## 🎓 Development Approach
1. Specification-driven development
2. AI-assisted coding with Claude Code
3. Modern full-stack architecture
4. API-first design
5. Component-based UI development

## 💰 Cost Optimization Strategies

1. **Efficient Model Selection**: Using gpt-4o-mini for optimal cost
2. **Token Limiting**: Controlling response lengths
3. **Batch Operations**: Efficient API usage patterns
4. **Caching**: Reducing redundant API calls

## 🏆 Completed Features
- **Phase I**: Console application with core task management
- **Phase II**: Full-stack web application with beautiful UI
- **Phase III**: AI chatbot with natural language processing
- **Advanced UI**: Glass morphism, animations, dark mode
- **Database Integration**: SQLModel with PostgreSQL
- **API Design**: RESTful endpoints with proper error handling
- **AI Integration**: OpenAI with function calling
- **Chat Interface**: Natural language task management
- **Authentication System**: User registration and login with JWT tokens
- **User Management**: Protected routes and user-specific data isolation
- **Deployment Ready**: Proper environment configuration

## 📦 Project Structure
```
hackathon-todo/
├── .env                         # Environment variables
├── frontend/                    # Next.js frontend application
│   ├── src/
│   │   └── app/
│   │       ├── components/      # React components
│   │       ├── chat/            # AI chat interface
│   │       │   └── components/  # Chat UI components
│   │       ├── login/           # Login page
│   │       ├── signup/          # Signup page
│   │       └── layout.tsx       # Global layout with navigation
│   ├── package.json
│   ├── next.config.js
│   └── tailwind.config.js
├── src/
│   ├── backend/                 # FastAPI backend
│   │   ├── main.py             # Main API application with auth routes
│   │   ├── models.py           # Database models (including User model)
│   │   ├── database.py         # Database configuration
│   │   ├── auth.py             # Authentication utilities
│   │   ├── openai_client.py    # OpenAI integration
│   │   ├── chat_routes.py      # AI chat API routes
│   │   ├── chat_models.py      # Chat data models
│   │   └── chat_queries.py     # Chat database operations
│   ├── ai_features.py          # AI functionality
│   └── task_manager.py         # Core task logic
├── WORK_SUMMARY.md             # Comprehensive work summary
├── constitution.md             # Core principles
└── CLAUDE.md                   # AI instructions
```

---

**Built with ❤️ using Spec-Driven Development and OpenAI Integration**
