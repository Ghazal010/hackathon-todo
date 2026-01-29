"""
AI-Powered Task Suggestion Module

This module demonstrates how OpenAI can be integrated into the todo app
for intelligent task suggestions and management.
"""

from typing import List, Dict, Optional
from src.openai_config import get_openai_manager
import json


def suggest_task_improvement(task_title: str, task_description: str = "") -> Optional[Dict[str, str]]:
    """
    Use OpenAI to suggest improvements to a task.

    Args:
        task_title: The title of the task
        task_description: The description of the task

    Returns:
        Dictionary with suggested improvements or None if API call fails
    """
    manager = get_openai_manager()

    prompt = f"""
    Analyze this todo task and provide suggestions for improvement:

    Task: {task_title}
    Description: {task_description}

    Respond with a JSON object containing:
    {{
        "title_suggestion": "Suggested improved title or null if current is good",
        "description_suggestion": "Suggested improved description or null if current is good",
        "priority_level": "low, medium, or high",
        "estimated_time": "Time estimate in minutes",
        "tags": ["list", "of", "relevant", "tags"]
    }}

    Be concise and practical with suggestions. If the task is already well-defined,
    you can suggest keeping it as is.
    """

    messages = [
        {"role": "user", "content": prompt}
    ]

    response = manager.chat_completion(messages)

    if response:
        try:
            # Extract JSON from response (may be wrapped in markdown)
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1

            if start_idx != -1 and end_idx != 0:
                json_str = response[start_idx:end_idx]
                suggestion = json.loads(json_str)
                return suggestion
        except json.JSONDecodeError:
            print("Failed to parse OpenAI response as JSON")
            return None

    return None


def generate_daily_tasks(context: str = "") -> Optional[List[Dict[str, str]]]:
    """
    Generate daily task suggestions based on context.

    Args:
        context: Context about the user's day/situation

    Returns:
        List of suggested tasks or None if API call fails
    """
    manager = get_openai_manager()

    prompt = f"""
    Based on this context, suggest 3-5 productive tasks for the day:

    Context: {context}

    Respond with a JSON array of objects like:
    [
        {{
            "title": "Task title",
            "description": "Brief description",
            "priority": "high, medium, or low"
        }}
    ]

    Keep suggestions practical and achievable.
    """

    messages = [
        {"role": "user", "content": prompt}
    ]

    response = manager.chat_completion(messages)

    if response:
        try:
            # Extract JSON from response
            start_idx = response.find('[')
            end_idx = response.rfind(']') + 1

            if start_idx != -1 and end_idx != 0:
                json_str = response[start_idx:end_idx]
                tasks = json.loads(json_str)
                return tasks
        except json.JSONDecodeError:
            print("Failed to parse OpenAI response as JSON")
            return None

    return None


def summarize_completed_tasks(task_list: List[Dict]) -> Optional[str]:
    """
    Summarize completed tasks for reflection.

    Args:
        task_list: List of task dictionaries

    Returns:
        Summary of completed tasks or None if API call fails
    """
    manager = get_openai_manager()

    completed_tasks = [task for task in task_list if task.get('completed', False)]

    if not completed_tasks:
        return "No tasks completed today."

    task_summaries = []
    for task in completed_tasks:
        task_summaries.append(f"- {task['title']}: {task.get('description', '')}")

    task_text = "\n".join(task_summaries)

    prompt = f"""
    Summarize these completed tasks and provide a brief reflection:

    {task_text}

    Keep the summary under 100 words and highlight productivity insights.
    """

    messages = [
        {"role": "user", "content": prompt}
    ]

    response = manager.chat_completion(messages)
    return response


def get_ai_productivity_tips(task_count: int) -> Optional[str]:
    """
    Get AI-powered productivity tips based on task statistics.

    Args:
        task_count: Number of tasks in the list

    Returns:
        Productivity tip or None if API call fails
    """
    manager = get_openai_manager()

    prompt = f"""
    Provide one concise productivity tip based on having {task_count} tasks in the list.
    Keep the tip under 50 words and make it actionable.
    """

    messages = [
        {"role": "user", "content": prompt}
    ]

    response = manager.chat_completion(messages)
    return response