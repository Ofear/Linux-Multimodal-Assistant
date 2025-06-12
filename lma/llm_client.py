"""Client interface for large language models.

This module will provide a minimal API wrapper around local or remote
LLM backends. Implementations may include HTTP requests or library
bindings to frameworks like HuggingFace transformers.
"""

from typing import Any


class LLMClient:
    """Placeholder LLM client."""

    def send_prompt(self, prompt: str) -> Any:
        """Send a prompt to the language model and return a response."""
        return None
