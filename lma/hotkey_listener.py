"""Hotkey listener for triggering assistant actions."""

from __future__ import annotations

from typing import Callable, Dict

try:
    from pynput import keyboard
except Exception:  # pragma: no cover - optional dependency
    keyboard = None


class HotkeyListener:
    """Listen for global hotkeys and dispatch callbacks."""

    def __init__(self, hotkeys: Dict[str, str], callback: Callable[[str], None]) -> None:
        self.callback = callback
        self.listener = None

        if keyboard:
            mappings = {v: (lambda name=k: self.callback(name)) for k, v in hotkeys.items()}
            self.listener = keyboard.GlobalHotKeys(mappings)

    def start(self) -> None:
        """Start listening for hotkeys."""
        if self.listener:
            self.listener.start()

    def stop(self) -> None:
        """Stop listening for hotkeys."""
        if self.listener:
            self.listener.stop()
            self.listener.join()
