"""Keyboard event injection utilities.

This module will allow the assistant to programmatically type text or
send keyboard shortcuts. Future implementations may rely on `pyautogui`
or `pynput`.
"""

class KeyboardInjector:
    """Simulate keyboard input using ``pyautogui``."""

    def __init__(self) -> None:
        try:
            import pyautogui

            self.pg = pyautogui
        except Exception:
            self.pg = None

    def type_text(self, text: str) -> None:
        """Simulate typing text on the keyboard."""
        if not self.pg:
            return
        try:
            self.pg.write(text)
        except Exception:
            pass

    def send_hotkey(self, *keys: str) -> None:
        """Send a keyboard shortcut."""
        if not self.pg:
            return
        try:
            self.pg.hotkey(*keys)
        except Exception:
            pass
