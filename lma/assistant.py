"""Main orchestrator for the Linux Multimodal Assistant."""

from __future__ import annotations

from typing import Optional

from . import mic_capture, transcribe, screenshot
from .llm_client import LLMClient
from .utils import load_config


class Assistant:
    """Coordinate user input, transcription and LLM querying."""

    def __init__(self, config_path: str = "config.json") -> None:
        self.config = load_config(config_path)
        self.llm = LLMClient(self.config)

    def run_once(self) -> Optional[str]:
        """Capture audio, transcribe it and query the LLM."""

        audio = mic_capture.record_audio()
        if not audio:
            return None

        text = transcribe.transcribe_audio(audio)
        if not text:
            return None

        response = self.llm.send_prompt(text)
        screenshot.take_screenshot(self.config)
        return response
