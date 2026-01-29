# Hackathon Todo App with OpenAI Integration

A todo application evolving from Python console app to cloud-native AI chatbot with OpenAI integration.

## 🎯 Project Goals
- Master Spec-Driven Development
- Build progressively complex software
- Learn cloud-native technologies
- Integrate OpenAI for enhanced productivity

## 📅 Timeline

| Phase | Description | Due Date | Status |
|-------|-------------|----------|--------|
| I | Python Console App | Dec 7, 2025 | ✅ Complete |
| II | Full-Stack Web App | Dec 14, 2025 | ⏳ Upcoming |
| III | AI Chatbot (OpenAI) | Dec 21, 2025 | ⏳ Upcoming |
| IV | Local Kubernetes | Jan 4, 2026 | ⏳ Upcoming |
| V | Cloud Deployment | Jan 18, 2026 | ⏳ Upcoming |

## 🛠️ Tech Stack

### Phase 1
- Python 3.13+
- UV package manager
- In-memory storage
- OpenAI integration for AI features

### Phase 2-5
- Next.js, FastAPI, Neon DB
- OpenAI GPT (instead of Gemini)
- Kubernetes, Kafka, Dapr

## 🚀 Getting Started
```bash
# Clone repository
git clone https://github.com/Ghazal010/hackathon-todo.git
cd hackathon-todo

# Install dependencies with UV
uv sync

# Set up OpenAI configuration
cp .env.example .env
# Edit .env to add your OpenAI API keys

# Run (Phase 1)
uv run python src/main.py
```

## ⚡ OpenAI Configuration for Minimal Usage

The application is configured to minimize API usage and stay within free tier limits:

- **Model**: Uses `gpt-3.5-turbo` which is most economical
- **Rate Limiting**: Limits requests to 3 per minute by default
- **Token Limit**: Caps response tokens at 150 to control costs
- **Key Rotation**: Automatically rotates between multiple API keys if provided
- **Retry Logic**: Attempts retries with different keys if one fails

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEYS` | Comma-separated list of API keys for rotation | (none) |
| `OPENAI_API_KEY` | Single API key (fallback if no multiple keys) | (none) |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-3.5-turbo` |
| `OPENAI_TEMPERATURE` | Creativity level (0.0-1.0) | `0.3` |
| `OPENAI_MAX_TOKENS` | Maximum tokens in response | `150` |
| `OPENAI_RPM_LIMIT` | Requests per minute limit | `3` |

## 📋 Features

### Phase 1: Basic Features
- ✅ Add Task
- ✅ Delete Task
- ✅ Update Task
- ✅ View Tasks
- ✅ Mark Complete
- ✅ AI Task Improvement

### AI-Powered Features
- **AI Task Enhancement**: Get suggestions to improve your task titles and descriptions
- **Smart Task Analysis**: AI analyzes tasks for better structure and clarity
- **Productivity Insights**: Get AI-powered tips based on your task patterns

## 🤖 AI Integration Details

The application includes AI-powered features to help you optimize your tasks:

1. **Add Task with AI**: Option to get AI suggestions when creating tasks
2. **AI Task Improvement**: Select existing tasks to get improvement suggestions
3. **Smart Suggestions**: AI provides structured recommendations for task refinement

## 📖 Documentation
- `constitution.md` - Core principles
- `CLAUDE.md` - AI instructions
- `specs/` - Feature specifications
- `src/openai_config.py` - OpenAI integration module
- `src/ai_features.py` - AI functionality

## 🎓 Spec-Driven Development
1. Write specification
2. Generate code with Claude Code (Qwen)
3. Test & validate
4. Refine if needed

**Rule**: No manual coding allowed.

## 💰 Cost Optimization Strategies

1. **Multiple Key Rotation**: Distribute requests across multiple accounts
2. **Conservative Token Usage**: Keep response lengths minimal
3. **Rate Limiting**: Prevent API limit exceeded errors
4. **Efficient Prompts**: Well-structured prompts for better results with fewer tokens
5. **Fallback Handling**: Graceful degradation if API calls fail

## 🏆 Scoring
- Phase I: 100 points
- Phase II: 150 points
- Phase III: 200 points
- Phase IV: 250 points
- Phase V: 300 points
- **Total**: 1000 points

## 📦 Project Structure
```
hackathon-todo/
├── specs/              # Specifications
├── src/                # Source code
│   ├── openai_config.py # OpenAI configuration
│   ├── ai_features.py   # AI functionality
│   └── ...
├── .env.example        # OpenAI configuration template
├── constitution.md     # Core principles
└── CLAUDE.md           # AI instructions
```

---

**Built with ❤️ using Spec-Driven Development and OpenAI Integration**
