"""User notification utilities.

This module will provide functionality for displaying desktop
notifications or other alerts to the user. Libraries such as
`notify2` or native system calls may be used.
"""

class Notifier:
    """Display desktop notifications."""

    def __init__(self) -> None:
        try:
            import notify2

            notify2.init("LMA")
            self.backend = notify2
        except Exception:
            self.backend = None

    def send(self, message: str) -> None:
        """Send a notification to the user."""
        if self.backend:
            try:
                n = self.backend.Notification("Assistant", message)
                n.set_timeout(3000)
                n.show()
                return
            except Exception:
                pass
        print(message)
