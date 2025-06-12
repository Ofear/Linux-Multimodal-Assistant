"""General utility functions used across modules."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


def load_config(path: str = "config.json") -> Dict[str, Any]:
    """Load configuration from ``path``.

    Parameters
    ----------
    path:
        Path to the JSON configuration file.

    Returns
    -------
    dict
        Parsed configuration dictionary. Returns an empty dict if the
        file does not exist or contains invalid JSON.
    """

    cfg_path = Path(path)
    if not cfg_path.exists():
        return {}

    try:
        with cfg_path.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except json.JSONDecodeError:
        return {}
