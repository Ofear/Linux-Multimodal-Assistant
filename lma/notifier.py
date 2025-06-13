"""User notification utilities.

This module provides functionality for displaying desktop notifications,
speaking responses via TTS, and showing confirmation dialogs.
"""

import subprocess
import shutil
from typing import Optional


class Notifier:
    """Display desktop notifications and speak responses."""

    def __init__(self, config: dict = None) -> None:
        self.config = config or {}
        self.tts_config = self.config.get("tts", {})
        
        # Initialize desktop notifications
        try:
            import notify2
            notify2.init("LMA")
            self.notify_backend = notify2
        except Exception:
            self.notify_backend = None

    def send(self, message: str) -> None:
        """Send a notification to the user."""
        # Show desktop notification
        self._show_notification(message)
        
        # Speak response if TTS is enabled
        if self.tts_config.get("enabled", True):
            self._speak(message)

    def _show_notification(self, message: str) -> None:
        """Display a desktop notification."""
        if self.notify_backend:
            try:
                n = self.notify_backend.Notification("Assistant", message)
                n.set_timeout(3000)
                n.show()
                return
            except Exception:
                pass
        
        # Fallback to print
        print(f"[Assistant] {message}")

    def _speak(self, text: str) -> None:
        """Speak text using TTS."""
        engine = self.tts_config.get("engine", "piper")
        
        if engine == "piper" and self._try_piper(text):
            return
        
        # Fallback to espeak
        fallback = self.tts_config.get("fallback", "espeak")
        if fallback == "espeak":
            self._try_espeak(text)

    def _try_piper(self, text: str) -> bool:
        """Try to speak using piper TTS."""
        try:
            import piper
            
            voice = self.tts_config.get("voice", "en_US-lessac-medium")
            
            # This is a simplified implementation - actual piper usage may vary
            # depending on the specific piper-tts installation
            if shutil.which("piper"):
                cmd = ["piper", "--model", voice, "--output-raw"]
                proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                proc.stdin.write(text.encode())
                proc.stdin.close()
                
                # Play the audio output (simplified - you might need aplay/paplay)
                if shutil.which("aplay"):
                    subprocess.run(["aplay", "-"], input=proc.stdout.read())
                elif shutil.which("paplay"):
                    subprocess.run(["paplay", "-"], input=proc.stdout.read())
                
                return True
        except Exception:
            pass
        
        return False

    def _try_espeak(self, text: str) -> None:
        """Speak using espeak as fallback."""
        if shutil.which("espeak"):
            try:
                subprocess.run(["espeak", text], check=True, 
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception:
                pass

    def confirm(self, message: str, title: str = "Confirmation") -> bool:
        """Show a confirmation dialog."""
        if shutil.which("zenity"):
            try:
                result = subprocess.run([
                    "zenity", "--question", 
                    "--title", title,
                    "--text", message,
                    "--width", "400"
                ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return result.returncode == 0
            except subprocess.CalledProcessError:
                return False
        
        # Fallback to terminal prompt
        try:
            response = input(f"{title}: {message} (y/N): ").strip().lower()
            return response in ['y', 'yes']
        except (EOFError, KeyboardInterrupt):
            return False

    def error(self, message: str) -> None:
        """Show an error dialog."""
        if shutil.which("zenity"):
            try:
                subprocess.run([
                    "zenity", "--error",
                    "--title", "Error",
                    "--text", message,
                    "--width", "400"
                ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return
            except Exception:
                pass
        
        # Fallback to notification
        self._show_notification(f"Error: {message}")

    def input_dialog(self, prompt: str, title: str = "Input") -> Optional[str]:
        """Show an input dialog."""
        if shutil.which("zenity"):
            try:
                result = subprocess.run([
                    "zenity", "--entry",
                    "--title", title,
                    "--text", prompt,
                    "--width", "400"
                ], check=True, capture_output=True, text=True)
                return result.stdout.strip()
            except subprocess.CalledProcessError:
                return None
        
        # Fallback to terminal input
        try:
            return input(f"{title}: {prompt}: ").strip()
        except (EOFError, KeyboardInterrupt):
            return None
