"""Client interface for large language models."""

from __future__ import annotations

from typing import Any, Dict

import httpx


class LLMClient:
    """Minimal client for remote or local LLM backends."""

    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config.get("llm", {})
        self.client = httpx.Client(timeout=30)

    def send_prompt(self, prompt: str) -> str:
        """Send ``prompt`` to the configured language model."""

        mode = self.config.get("mode", "gpt-4o")
        if mode == "gpt-4o":
            return self._call_openai(prompt)
        return self._call_local(prompt)

    # ------------------------------------------------------------------
    def _call_openai(self, prompt: str) -> str:
        headers = {"Authorization": f"Bearer {self.config.get('openai_api_key', '')}"}
        payload = {
            "model": "gpt-4o",
            "messages": [{"role": "user", "content": prompt}],
        }
        resp = self.client.post(
            "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]

    def _call_local(self, prompt: str) -> str:
        url = self.config.get("local_endpoint", "http://localhost:11434")
        payload = {"model": self.config.get("primary_local_model", "llava"), "prompt": prompt}
        resp = self.client.post(url, json=payload)
        resp.raise_for_status()
        data = resp.json()
        return data.get("response", "")
