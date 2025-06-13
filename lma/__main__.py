#!/usr/bin/env python3
"""Main entry point for the Linux Multimodal Assistant."""

import sys
import time
import signal
from typing import Optional

from .assistant import Assistant
from .hotkey_listener import HotkeyListener
from .utils import load_config


class MultimodalAssistant:
    """Main application coordinator."""

    def __init__(self, config_path: str = "config.json") -> None:
        self.config = load_config(config_path)
        self.assistant = Assistant(config_path)
        self.hotkey_listener: Optional[HotkeyListener] = None
        self.running = False

    def handle_hotkey(self, action: str) -> None:
        """Handle hotkey activation with proper workflow differentiation."""
        self.assistant.logger.info(f"Hotkey activated: {action}")
        
        try:
            if action == "activate":
                # Full multimodal capture (screenshot + audio) - Ctrl+Alt+A
                self.assistant.handle_multimodal_input()
            elif action == "voice_input":
                # Voice-only input (no screenshot) - Ctrl+Alt+M
                self.assistant.handle_voice_only()
            elif action == "text_selection":
                # Process selected text - Ctrl+Alt+V
                self.assistant.handle_text_selection()
            else:
                self.assistant.logger.warning(f"Unknown hotkey action: {action}")
                self.assistant.notifier.error(f"Unknown hotkey action: {action}")
        except Exception as e:
            error_msg = f"Error processing {action}: {str(e)}"
            self.assistant.logger.error(error_msg)
            self.assistant.notifier.error(f"Processing failed: {str(e)}")

    def start(self) -> None:
        """Start the assistant service."""
        self.assistant.logger.info("Starting Linux Multimodal Assistant")
        
        # Set up hotkey listener
        hotkeys = self.config.get("hotkeys", {})
        if hotkeys:
            self.hotkey_listener = HotkeyListener(hotkeys, self.handle_hotkey)
            self.hotkey_listener.start()
            self.assistant.logger.info(f"Hotkeys registered: {list(hotkeys.keys())}")
            
            # Log hotkey mappings for user reference
            for action, key_combination in hotkeys.items():
                if action != "allow_custom":  # Skip non-hotkey config
                    self.assistant.logger.info(f"  {action}: {key_combination}")
        else:
            self.assistant.logger.warning("No hotkeys configured")
            self.assistant.notifier.error("No hotkeys configured in config.json")

        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        self.running = True
        
        # Welcome message
        welcome_msg = "Linux Multimodal Assistant is running! Available hotkeys:\n"
        hotkey_descriptions = {
            "activate": "Full multimodal (screenshot + voice)",
            "voice_input": "Voice-only input",
            "text_selection": "Process selected text"
        }
        
        for action, key_combination in hotkeys.items():
            if action in hotkey_descriptions:
                welcome_msg += f"  {key_combination}: {hotkey_descriptions[action]}\n"
        
        welcome_msg += "Press Ctrl+C to stop."
        
        self.assistant.logger.info("Assistant is running. Press Ctrl+C to stop.")
        print(welcome_msg)
        
        try:
            # Main loop
            while self.running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            pass
        finally:
            self.stop()

    def stop(self) -> None:
        """Stop the assistant service."""
        self.assistant.logger.info("Stopping Linux Multimodal Assistant")
        self.running = False
        
        if self.hotkey_listener:
            self.hotkey_listener.stop()

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        self.assistant.logger.info(f"Received signal {signum}, shutting down...")
        self.stop()


def main() -> None:
    """Main entry point."""
    try:
        app = MultimodalAssistant()
        app.start()
    except Exception as e:
        print(f"Error starting assistant: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main() 