"""Mouse control utilities for automation.

In the future this module may use `pyautogui` or similar libraries to
simulate mouse movement and clicks. Currently it provides a placeholder
class interface.
"""

class MouseController:
    """Placeholder mouse controller."""

    def move(self, x: int, y: int) -> None:
        """Move the mouse to the given coordinates."""
        pass

    def click(self) -> None:
        """Perform a mouse click."""
        pass
