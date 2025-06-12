"""Clipboard management utilities.

Functions in this module will interact with the system clipboard to
retrieve and set text or other data formats. Future implementations may
use `pyperclip` or platform specific commands.
"""


def get_clipboard() -> str:
    """Return the current clipboard contents."""
    try:
        import pyperclip

        return pyperclip.paste() or ""
    except Exception:
        return ""


def set_clipboard(text: str) -> None:
    """Set the clipboard contents."""
    try:
        import pyperclip

        pyperclip.copy(text)
    except Exception:
        pass
