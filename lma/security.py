"""Security and command sanitization utilities."""

from __future__ import annotations

import re
from typing import List, Optional


def sanitize_text(text: str) -> str:
    """Remove potentially dangerous patterns from text."""
    if not text:
        return ""
    
    # Remove shell injection patterns
    dangerous_patterns = [
        r';\s*rm\s+',
        r'&&\s*rm\s+',
        r'\|\s*rm\s+',
        r'`[^`]*`',
        r'\$\([^)]*\)',
        r'>\s*/dev/',
        r'<\s*/dev/',
        r'\|\s*sh\s*',
        r'\|\s*bash\s*',
        r';\s*sudo\s+',
        r'&&\s*sudo\s+',
    ]
    
    sanitized = text
    for pattern in dangerous_patterns:
        sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
    
    return sanitized.strip()


def is_safe_command(command: str, config: dict) -> bool:
    """Check if a command is in the allowed list."""
    if not command:
        return False
    
    # Get the base command (first word)
    base_cmd = command.strip().split()[0]
    
    # Check against allowed commands
    allowed = config.get("security", {}).get("allow_commands", [])
    return base_cmd in allowed


def requires_confirmation(command: str, config: dict) -> bool:
    """Check if a command requires user confirmation."""
    if not command:
        return False
    
    # Get the base command (first word)
    base_cmd = command.strip().split()[0]
    
    # Check against commands requiring confirmation
    confirm_required = config.get("security", {}).get("confirm_required", [])
    return base_cmd in confirm_required


def validate_coordinates(x: int, y: int, screen_width: int = 1920, screen_height: int = 1080) -> bool:
    """Validate mouse coordinates are within reasonable bounds."""
    return (0 <= x <= screen_width and 0 <= y <= screen_height)


def extract_commands(text: str) -> List[str]:
    """Extract potential shell commands from text."""
    # Look for patterns that might be commands
    command_patterns = [
        r'(?:^|\n)([a-zA-Z][a-zA-Z0-9_-]*(?:\s+[^\n]*)?)',  # Basic command pattern
        r'`([^`]+)`',  # Backtick commands
        r'\$\(([^)]+)\)',  # Command substitution
    ]
    
    commands = []
    for pattern in command_patterns:
        matches = re.finditer(pattern, text, re.MULTILINE)
        for match in matches:
            cmd = match.group(1).strip()
            if cmd and not cmd.startswith('#'):  # Skip comments
                commands.append(cmd)
    
    return commands


def sanitize_input(text: str, config: dict) -> str:
    """Sanitize input text according to security settings."""
    if not config.get("security", {}).get("sanitize_inputs", True):
        return text
    
    return sanitize_text(text)


def redact_sensitive_data(log_message: str, config: dict) -> str:
    """Redact sensitive information from log messages."""
    if not config.get("logging", {}).get("redact_sensitive", True):
        return log_message
    
    # Redact API keys
    redacted = re.sub(r'sk-[a-zA-Z0-9]{48,}', 'sk-***REDACTED***', log_message)
    
    # Redact potential passwords or tokens
    redacted = re.sub(r'(password|token|key|secret)["\s]*[:=]["\s]*[^\s"]+', 
                     r'\1: ***REDACTED***', redacted, flags=re.IGNORECASE)
    
    return redacted
