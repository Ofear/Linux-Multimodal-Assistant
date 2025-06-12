"""Mouse control utilities for automation."""

from __future__ import annotations

import shutil
import subprocess


def _which(cmd: str) -> bool:
    return shutil.which(cmd) is not None

class MouseController:
    """Control the mouse pointer."""

    def __init__(self) -> None:
        self.xdotool = _which("xdotool")
        self.ydotool = _which("ydotool")
        try:
            import pyautogui

            self.pg = pyautogui
        except Exception:  # pragma: no cover - optional dependency
            self.pg = None

    def move(self, x: int, y: int) -> None:
        """Move the mouse to the given coordinates."""
        if self.xdotool:
            subprocess.run(["xdotool", "mousemove", str(x), str(y)], check=False)
        elif self.ydotool:
            subprocess.run(["ydotool", "mousemove", str(x), str(y)], check=False)
        elif self.pg:
            try:
                self.pg.moveTo(x, y)
            except Exception:
                pass

    def click(self) -> None:
        """Perform a mouse click."""
        if self.xdotool:
            subprocess.run(["xdotool", "click", "1"], check=False)
        elif self.ydotool:
            subprocess.run(["ydotool", "click", "1"], check=False)
        elif self.pg:
            try:
                self.pg.click()
            except Exception:
                pass
