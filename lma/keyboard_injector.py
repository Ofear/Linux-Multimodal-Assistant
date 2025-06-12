"""Keyboard event injection utilities.

This module will allow the assistant to programmatically type text or
send keyboard shortcuts. Future implementations may rely on `pyautogui`
or `pynput`.
"""

class KeyboardInjector:
    """Placeholder keyboard injector."""

    def type_text(self, text: str) -> None:
        """Simulate typing text on the keyboard."""
        _ = text

    def send_hotkey(self, *keys: str) -> None:
        """Send a keyboard shortcut."""
        _ = keys
