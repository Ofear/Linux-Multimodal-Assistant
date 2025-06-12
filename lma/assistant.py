"""Main orchestrator for the Linux Multimodal Assistant."""

from __future__ import annotations

from typing import Optional

from . import mic_capture, transcribe, screenshot, clipboard
from .llm_client import LLMClient
from .utils import load_config, compress_image
from .notifier import Notifier
from .mouse_controller import MouseController
from .keyboard_injector import KeyboardInjector


class Assistant:
    """Coordinate user input, transcription and LLM querying."""

    def __init__(self, config_path: str = "config.json") -> None:
        self.config = load_config(config_path)
        self.llm = LLMClient(self.config)
        self.notifier = Notifier()
        self.mouse = MouseController()
        self.keyboard = KeyboardInjector()

    def run_once(self) -> Optional[str]:
        """Capture audio, transcribe it and query the LLM."""

        audio = mic_capture.record_audio()
        if not audio:
            return None

        text = transcribe.transcribe_audio(audio)
        if not text:
            return None

        clip = clipboard.get_clipboard()
        prompt = text
        if clip:
            prompt = f"{text}\n\n{clip}"

        shot = screenshot.take_screenshot(self.config)
        if shot:
            compress_image(shot, 80)

        response = self.llm.send_prompt(prompt, image_path=shot)
        self.notifier.send(response)
        return response
