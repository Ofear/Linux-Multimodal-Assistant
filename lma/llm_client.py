"""Client interface for large language models."""

from __future__ import annotations

from typing import Any, Dict, Optional

import httpx


class LLMClient:
    """Minimal client for remote or local LLM backends."""

    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config.get("llm", {})
        self.client = httpx.Client(timeout=30)
        self.retries = 3

    def send_prompt(self, prompt: str, image_path: Optional[str] = None) -> str:
        """Send ``prompt`` to the configured language model."""

        mode = self.config.get("mode", "gpt-4o")
        if mode == "gpt-4o":
            try:
                return self._call_openai(prompt, image_path)
            except Exception:
                return self._call_local(prompt, image_path)
        try:
            return self._call_local(prompt, image_path)
        except Exception:
            return self._call_openai(prompt, image_path)

    # ------------------------------------------------------------------
    def _call_openai(self, prompt: str, image_path: Optional[str] = None) -> str:
        headers = {"Authorization": f"Bearer {self.config.get('openai_api_key', '')}"}
        payload = {
            "model": "gpt-4o",
            "messages": [{"role": "user", "content": prompt}],
        }
        def make_request(files: Optional[dict]) -> str:
            for _ in range(self.retries):
                try:
                    resp = self.client.post(
                        "https://api.openai.com/v1/chat/completions",
                        headers=headers,
                        json=payload,
                        files=files,
                    )
                    resp.raise_for_status()
                    data = resp.json()
                    return data["choices"][0]["message"]["content"]
                except httpx.HTTPError:
                    continue
            raise RuntimeError("OpenAI API request failed")

        if image_path:
            with open(image_path, "rb") as fh:
                return make_request({"file": fh})
        return make_request(None)
        raise RuntimeError("OpenAI API request failed")

    def _call_local(self, prompt: str, image_path: Optional[str] = None) -> str:
        url = self.config.get("local_endpoint", "http://localhost:11434")
        payload = {
            "model": self.config.get("primary_local_model", "llava"),
            "prompt": prompt,
        }
        def make_request(files: Optional[dict]) -> str:
            for _ in range(self.retries):
                try:
                    resp = self.client.post(url, json=payload, files=files)
                    resp.raise_for_status()
                    data = resp.json()
                    return data.get("response", "")
                except httpx.HTTPError:
                    continue
            raise RuntimeError("Local LLM request failed")

        if image_path:
            with open(image_path, "rb") as fh:
                return make_request({"image": fh})
        return make_request(None)
