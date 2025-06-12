"""Security related helpers for the assistant."""

from __future__ import annotations

import re
from typing import Any, Dict


def sanitize_command(cmd: str) -> str:
    """Remove common shell metacharacters from ``cmd``."""

    return re.sub(r"[;&|`$<>]", "", cmd)


def requires_confirmation(cmd: str, config: Dict[str, Any]) -> bool:
    """Return ``True`` if ``cmd`` should be confirmed by the user."""

    confirm = set(config.get("security", {}).get("confirm_required", []))
    base = cmd.split()[0]
    return base in confirm


def is_command_allowed(cmd: str, config: Dict[str, Any]) -> bool:
    """Check whether the base command is whitelisted."""

    allowed = set(config.get("security", {}).get("allow_commands", []))
    base = cmd.split()[0]
    return base in allowed


def sanitize_text(text: str) -> str:
    """Remove obvious shell injection patterns from ``text``."""

    return re.sub(r"[;&|`$<>]", "", text)
