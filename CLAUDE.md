# Claude Code Instructions for Hackathon Todo

## Project Overview
This is a **Spec-Driven Development** project where you (Claude Code via Qwen) generate all implementation code based on specifications.

## Your Role
1. Read specifications from /specs/ folder
2. Generate clean, working Python/JavaScript code
3. Follow the project constitution
4. Ask clarifying questions if specs are unclear

## Current Phase: Phase 1
- **Goal**: Build in-memory Python console Todo app
- **Tech**: Python 3.13+, UV package manager
- **Features**: Add, Delete, Update, View, Mark Complete

## Code Quality Standards

### Python Requirements
- Type hints for all functions
- Docstrings in Google style
- Input validation with clear errors
- Meaningful variable names
- Error handling with try/except

### Example:
```python
from typing import Optional

def add_task(title: str, description: Optional[str] = None) -> dict:
    """
    Add a new task to the task list.
    
    Args:
        title: Task title (required, 1-200 characters)
        description: Task description (optional)
        
    Returns:
        dict: Created task with id, title, description, completed
    """
    if not title or len(title) > 200:
        raise ValueError("Title must be 1-200 characters")
    
    task = {
        "id": generate_id(),
        "title": title,
        "description": description or "",
        "completed": False
    }
    return task
```

## Workflow
1. Locate spec: specs/phase1/features/[feature].md
2. Read acceptance criteria
3. Generate code meeting ALL criteria
4. Include error handling and type hints

## Key Principles
- Specs → Code (never reverse)
- Quality over speed
- Ask if unclear

---

**Let's build something great! 🚀**
