"""Main orchestrator for the Linux Multimodal Assistant."""

from __future__ import annotations

from typing import Optional

from . import mic_capture, transcribe, screenshot, clipboard
from .llm_client import LLMClient
from .utils import load_config, compress_image, setup_logging
from .security import sanitize_text
from .notifier import Notifier
from .mouse_controller import MouseController
from .keyboard_injector import KeyboardInjector


class Assistant:
    """Coordinate user input, transcription and LLM querying."""

    def __init__(self, config_path: str = "config.json") -> None:
        self.config = load_config(config_path)
        self.logger = setup_logging(self.config)
        self.llm = LLMClient(self.config)
        self.notifier = Notifier()
        self.mouse = MouseController()
        self.keyboard = KeyboardInjector()

    def run_once(self) -> Optional[str]:
        """Capture audio, transcribe it and query the LLM."""
        self.logger.info("Recording audio")
        audio = mic_capture.record_audio()
        if not audio:
            self.logger.error("Audio capture failed")
            return None

        text = transcribe.transcribe_audio(audio)
        if not text:
            self.logger.error("Transcription failed")
            return None

        clip = clipboard.get_clipboard()
        prompt = text
        if clip:
            prompt = f"{text}\n\n{clip}"

        shot = screenshot.take_screenshot(self.config)
        if shot:
            compress_image(shot, 80)

        self.logger.info("Sending prompt to LLM")
        response = self.llm.send_prompt(prompt, image_path=shot)
        response = sanitize_text(response)
        self.notifier.send(response)
        return response
