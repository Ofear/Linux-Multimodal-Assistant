"""Main orchestrator for the Linux Multimodal Assistant."""

from __future__ import annotations

import subprocess
import re
from typing import Optional

from . import mic_capture, transcribe, screenshot, clipboard
from .llm_client import LLMClient
from .utils import load_config, compress_image, setup_logging
from .security import sanitize_text, extract_commands, is_safe_command, requires_confirmation, sanitize_input, redact_sensitive_data, validate_coordinates
from .notifier import Notifier
from .mouse_controller import MouseController
from .keyboard_injector import KeyboardInjector


class Assistant:
    """Coordinate user input, transcription and LLM querying."""

    def __init__(self, config_path: str = "config.json") -> None:
        self.config = load_config(config_path)
        self.logger = setup_logging(self.config)
        self.llm = LLMClient(self.config)
        self.notifier = Notifier(self.config)  # Pass config for TTS
        self.mouse = MouseController()
        self.keyboard = KeyboardInjector()

    def handle_multimodal_input(self) -> Optional[str]:
        """Handle full multimodal input (screenshot + voice) - Ctrl+Alt+A."""
        self.logger.info("Processing multimodal input (screenshot + voice)")
        
        # Capture screenshot first
        shot = screenshot.take_screenshot(self.config)
        if shot:
            compress_image(shot, 80)
            self.logger.info(f"Screenshot captured: {shot}")
        else:
            self.logger.warning("Screenshot capture failed")

        # Record audio
        self.logger.info("Recording audio")
        audio = mic_capture.record_audio()
        if not audio:
            self.logger.error("Audio capture failed")
            self.notifier.error("Audio capture failed")
            return None

        # Transcribe audio
        text = transcribe.transcribe_audio(audio)
        if not text:
            self.logger.error("Transcription failed")
            self.notifier.error("Transcription failed")
            return None

        self.logger.info(f"Transcribed text: {redact_sensitive_data(text, self.config)}")

        # Get clipboard content
        clip = clipboard.get_clipboard()
        prompt = text
        if clip:
            prompt = f"{text}\n\nContext: {clip}"

        # Send to LLM with image
        response = self._query_llm(prompt, image_path=shot)
        return self._process_response(response)

    def handle_voice_only(self) -> Optional[str]:
        """Handle voice-only input (no screenshot) - Ctrl+Alt+M."""
        self.logger.info("Processing voice-only input")
        
        # Record audio
        self.logger.info("Recording audio")
        audio = mic_capture.record_audio()
        if not audio:
            self.logger.error("Audio capture failed")
            self.notifier.error("Audio capture failed")
            return None

        # Transcribe audio
        text = transcribe.transcribe_audio(audio)
        if not text:
            self.logger.error("Transcription failed")
            self.notifier.error("Transcription failed")
            return None

        self.logger.info(f"Transcribed text: {redact_sensitive_data(text, self.config)}")

        # Send to LLM without image
        response = self._query_llm(text)
        return self._process_response(response)

    def handle_text_selection(self) -> Optional[str]:
        """Handle text selection processing - Ctrl+Alt+V."""
        self.logger.info("Processing text selection")
        
        # Get selected text
        selected_text = clipboard.get_clipboard()
        if not selected_text:
            self.logger.warning("No text selected")
            self.notifier.error("No text selected or clipboard is empty")
            return None

        # Get additional voice command for what to do with the text
        self.notifier.send("Selected text captured. Please provide a voice command for what to do with it.")
        
        audio = mic_capture.record_audio()
        if not audio:
            self.logger.error("Audio capture failed")
            self.notifier.error("Audio capture failed")
            return None

        command = transcribe.transcribe_audio(audio)
        if not command:
            self.logger.error("Transcription failed")
            self.notifier.error("Transcription failed")
            return None

        self.logger.info(f"Voice command: {redact_sensitive_data(command, self.config)}")

        # Combine command with selected text
        prompt = f"{command}\n\nText to process: {selected_text}"
        
        # Send to LLM
        response = self._query_llm(prompt)
        processed_response = self._process_response(response)
        
        # Replace clipboard with the response
        if processed_response:
            clipboard.set_clipboard(processed_response)
            self.notifier.send("Clipboard updated with processed text")
        
        return processed_response

    def _query_llm(self, prompt: str, image_path: Optional[str] = None) -> str:
        """Query the LLM with sanitized input."""
        sanitized_prompt = sanitize_input(prompt, self.config)
        
        self.logger.info("Sending prompt to LLM")
        try:
            response = self.llm.send_prompt(sanitized_prompt, image_path=image_path)
            return response
        except Exception as e:
            error_msg = f"LLM query failed: {str(e)}"
            self.logger.error(error_msg)
            self.notifier.error("Failed to get response from AI")
            return ""

    def _process_response(self, response: str) -> Optional[str]:
        """Process and handle LLM response, including security checks and automation."""
        if not response:
            return None

        # Sanitize the response
        sanitized_response = sanitize_text(response)
        
        # Check for automation commands first
        self._handle_automation_commands(sanitized_response)
        
        # Check for shell commands
        commands = extract_commands(sanitized_response)
        if commands:
            self.logger.info(f"Found {len(commands)} potential commands in response")
            
            for cmd in commands:
                if not is_safe_command(cmd, self.config):
                    self.logger.warning(f"Unsafe command detected: {cmd}")
                    continue
                
                if requires_confirmation(cmd, self.config):
                    if not self.notifier.confirm(
                        f"Execute command: {cmd}?",
                        "Security Confirmation"
                    ):
                        self.logger.info(f"User denied command execution: {cmd}")
                        continue
                
                # Execute the command
                self._execute_shell_command(cmd)

        # Send the response to user
        self.notifier.send(sanitized_response)
        self.logger.info(f"Response sent: {redact_sensitive_data(sanitized_response, self.config)}")
        
        return sanitized_response

    def _handle_automation_commands(self, response: str) -> None:
        """Handle mouse and keyboard automation commands from LLM response."""
        
        # Look for mouse click commands: "click at (x, y)" or "click coordinates x,y"
        click_patterns = [
            r'click\s+(?:at\s+)?\(?(\d+),\s*(\d+)\)?',
            r'click\s+coordinates\s+(\d+),\s*(\d+)',
            r'move\s+to\s+(\d+),\s*(\d+)\s+and\s+click'
        ]
        
        for pattern in click_patterns:
            matches = re.finditer(pattern, response, re.IGNORECASE)
            for match in matches:
                try:
                    x, y = int(match.group(1)), int(match.group(2))
                    if validate_coordinates(x, y):
                        self.logger.info(f"Executing mouse click at ({x}, {y})")
                        self.mouse.move(x, y)
                        self.mouse.click()
                    else:
                        self.logger.warning(f"Invalid coordinates: ({x}, {y})")
                except (ValueError, IndexError):
                    continue
        
        # Look for mouse move commands: "move to (x, y)" or "move mouse to x,y"
        move_patterns = [
            r'move\s+(?:mouse\s+)?to\s+\(?(\d+),\s*(\d+)\)?',
            r'move\s+cursor\s+to\s+(\d+),\s*(\d+)'
        ]
        
        for pattern in move_patterns:
            matches = re.finditer(pattern, response, re.IGNORECASE)
            for match in matches:
                try:
                    x, y = int(match.group(1)), int(match.group(2))
                    if validate_coordinates(x, y):
                        self.logger.info(f"Moving mouse to ({x}, {y})")
                        self.mouse.move(x, y)
                    else:
                        self.logger.warning(f"Invalid coordinates: ({x}, {y})")
                except (ValueError, IndexError):
                    continue
        
        # Look for typing commands: "type text 'hello world'" or "enter text: hello world"
        type_patterns = [
            r'type\s+(?:text\s+)?["\']([^"\']+)["\']',
            r'enter\s+text:\s*(.+?)(?:\n|$)',
            r'input\s+text\s+["\']([^"\']+)["\']'
        ]
        
        for pattern in type_patterns:
            matches = re.finditer(pattern, response, re.IGNORECASE)
            for match in matches:
                text_to_type = match.group(1).strip()
                if text_to_type:
                    self.logger.info(f"Typing text: {redact_sensitive_data(text_to_type, self.config)}")
                    self.keyboard.type_text(text_to_type)
        
        # Look for hotkey commands: "press ctrl+c" or "send hotkey alt+tab"
        hotkey_patterns = [
            r'press\s+((?:\w+\+)*\w+)',
            r'send\s+hotkey\s+((?:\w+\+)*\w+)',
            r'use\s+keyboard\s+shortcut\s+((?:\w+\+)*\w+)'
        ]
        
        for pattern in hotkey_patterns:
            matches = re.finditer(pattern, response, re.IGNORECASE)
            for match in matches:
                hotkey = match.group(1).strip()
                if hotkey:
                    # Convert to pyautogui format
                    keys = [key.strip().lower() for key in hotkey.split('+')]
                    self.logger.info(f"Sending hotkey: {hotkey}")
                    self.keyboard.send_hotkey(*keys)

    def _execute_shell_command(self, command: str) -> None:
        """Execute a shell command safely."""
        self.logger.info(f"Executing shell command: {command}")
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,  # 30 second timeout
                check=False
            )
            
            if result.returncode == 0:
                if result.stdout:
                    output = result.stdout.strip()
                    self.logger.info(f"Command output: {output}")
                    self.notifier.send(f"Command executed successfully: {output}")
                else:
                    self.notifier.send("Command executed successfully")
            else:
                error_msg = result.stderr.strip() if result.stderr else f"Command failed with code {result.returncode}"
                self.logger.error(f"Command failed: {error_msg}")
                self.notifier.error(f"Command failed: {error_msg}")
                
        except subprocess.TimeoutExpired:
            self.logger.error(f"Command timed out: {command}")
            self.notifier.error("Command execution timed out")
        except Exception as e:
            self.logger.error(f"Command execution error: {str(e)}")
            self.notifier.error(f"Command execution error: {str(e)}")

    # Backward compatibility method
    def run_once(self) -> Optional[str]:
        """Legacy method for backward compatibility - defaults to multimodal input."""
        return self.handle_multimodal_input()
