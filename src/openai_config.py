"""
OpenAI Configuration Module for Minimal API Usage

This module handles OpenAI API key management and minimal usage strategies
to stay within free tier limits using multiple account keys.
"""

import os
from typing import List, Optional
import openai
from dataclasses import dataclass
from itertools import cycle
import time


@dataclass
class OpenAIConfig:
    """Configuration for OpenAI API usage with minimal consumption."""

    # Multiple API keys for load balancing across accounts
    api_keys: List[str]
    # Model to use (gpt-3.5-turbo is cheapest for most tasks)
    model: str = "gpt-3.5-turbo"
    # Temperature for creativity (0.0 = deterministic, higher = more creative)
    temperature: float = 0.3
    # Maximum tokens to save costs
    max_tokens: int = 150
    # Timeout settings
    timeout: int = 10
    # Rate limiting (requests per minute)
    rpm_limit: int = 3
    # Last request timestamp for rate limiting
    last_request_time: float = 0.0

    def __post_init__(self):
        """Initialize the OpenAI client with the first available key."""
        if self.api_keys:
            self._setup_client(self.api_keys[0])
            self.key_cycle = cycle(self.api_keys)
        else:
            # Fallback to environment variable
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                self._setup_client(api_key)
                self.key_cycle = cycle([api_key])
            else:
                raise ValueError(
                    "No OpenAI API keys provided. Set OPENAI_API_KEYS environment variable "
                    "with comma-separated keys or provide keys in constructor."
                )

    def _setup_client(self, api_key: str):
        """Setup OpenAI client with the given API key."""
        openai.api_key = api_key

    def get_next_key(self) -> str:
        """Get the next API key in rotation."""
        return next(self.key_cycle)

    def rotate_key(self):
        """Rotate to the next API key."""
        next_key = self.get_next_key()
        self._setup_client(next_key)
        return next_key

    def enforce_rate_limit(self):
        """Enforce rate limiting to stay within API limits."""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time

        # Calculate minimum time between requests (in seconds)
        min_interval = 60.0 / self.rpm_limit

        if time_since_last_request < min_interval:
            sleep_time = min_interval - time_since_last_request
            time.sleep(sleep_time)

        self.last_request_time = time.time()


class OpenAIManager:
    """Manages OpenAI API calls with minimal usage strategies."""

    def __init__(self, config: OpenAIConfig):
        self.config = config
        self.usage_stats = {"calls_made": 0, "tokens_used": 0}

    def chat_completion(self, messages: List[dict], **kwargs) -> Optional[str]:
        """
        Make a chat completion call with minimal usage.

        Args:
            messages: List of messages in the conversation
            **kwargs: Additional parameters to override config

        Returns:
            Response content or None if failed
        """
        # Enforce rate limiting
        self.config.enforce_rate_limit()

        # Override config with kwargs if provided
        params = {
            "model": self.config.model,
            "messages": messages,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            "timeout": self.config.timeout,
        }
        params.update(kwargs)

        max_retries = len(self.config.api_keys)  # Try each key once

        for attempt in range(max_retries):
            try:
                response = openai.chat.completions.create(**params)

                # Update usage stats
                self.usage_stats["calls_made"] += 1
                # Approximate token usage (actual usage might differ)
                tokens_used = sum(len(msg.get("content", "").split()) for msg in messages)
                tokens_used += len(response.choices[0].message.content.split())
                self.usage_stats["tokens_used"] += tokens_used

                return response.choices[0].message.content

            except Exception as e:
                print(f"API call failed with key (attempt {attempt + 1}): {str(e)}")

                # Rotate to next key for retry
                if attempt < max_retries - 1:
                    new_key = self.config.rotate_key()
                    print(f"Rotating to next API key: {new_key[-4:] if new_key else 'None'}")
                else:
                    print("All API keys exhausted. Request failed.")
                    return None

        return None

    def get_usage_summary(self) -> dict:
        """Get a summary of API usage."""
        return self.usage_stats


def initialize_openai_manager() -> OpenAIManager:
    """
    Initialize OpenAI manager with configuration from environment variables.

    Environment variables:
    - OPENAI_API_KEYS: Comma-separated list of API keys
    - OPENAI_MODEL: Model to use (default: gpt-3.5-turbo)
    - OPENAI_TEMPERATURE: Temperature setting (default: 0.3)
    - OPENAI_MAX_TOKENS: Maximum tokens (default: 150)
    - OPENAI_RPM_LIMIT: Requests per minute limit (default: 3)
    """
    # Get API keys from environment
    api_keys_str = os.getenv("OPENAI_API_KEYS", "")
    if not api_keys_str:
        # Fallback to single key
        single_key = os.getenv("OPENAI_API_KEY", "")
        api_keys = [single_key] if single_key else []
    else:
        api_keys = [key.strip() for key in api_keys_str.split(",") if key.strip()]

    # Get other config from environment
    model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    temperature = float(os.getenv("OPENAI_TEMPERATURE", "0.3"))
    max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", "150"))
    rpm_limit = int(os.getenv("OPENAI_RPM_LIMIT", "3"))

    config = OpenAIConfig(
        api_keys=api_keys,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        rpm_limit=rpm_limit
    )

    return OpenAIManager(config)


# Global instance for easy access
openai_manager: Optional[OpenAIManager] = None


def get_openai_manager() -> OpenAIManager:
    """Get the global OpenAI manager instance."""
    global openai_manager
    if openai_manager is None:
        openai_manager = initialize_openai_manager()
    return openai_manager