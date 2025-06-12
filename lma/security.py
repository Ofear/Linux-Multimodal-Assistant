"""Security related helpers for the assistant."""

from __future__ import annotations

import re
from typing import Any, Dict


def sanitize_command(cmd: str) -> str:
    """Remove common shell metacharacters from ``cmd``."""

    return re.sub(r"[;&|`$<>]", "", cmd)


def is_command_allowed(cmd: str, config: Dict[str, Any]) -> bool:
    """Check whether the base command is whitelisted."""

    allowed = set(config.get("security", {}).get("allow_commands", []))
    base = cmd.split()[0]
    return base in allowed
