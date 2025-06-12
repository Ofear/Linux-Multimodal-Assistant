"""General utility functions used across modules."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict
try:  # optional
    from PIL import Image
except Exception:  # pragma: no cover
    Image = None


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


def compress_image(path: str, quality: int = 80) -> None:
    """Compress ``path`` in-place as JPEG with ``quality``."""

    if Image is None:
        return
    try:
        img = Image.open(path)
        img.save(path, format="JPEG", quality=quality)
    except Exception:
        pass
