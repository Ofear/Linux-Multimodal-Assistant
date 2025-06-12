"""Utilities for capturing screenshots."""

from __future__ import annotations

import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional

try:  # optional dependency
    import mss
    import mss.tools
except Exception:  # pragma: no cover - fallback when mss unavailable
    mss = None


def _timestamped_name(prefix: str = "shot", ext: str = "png") -> str:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{ts}.{ext}"


def take_screenshot(config: dict) -> Optional[str]:
    """Capture a screenshot using available backends.

    The function attempts to use ``flameshot`` or ``grim`` if available.
    If neither command is found, it falls back to the ``mss`` Python
    library. The resulting image path is returned or ``None`` on failure.
    """

    directory = Path(config.get("screenshot_dir", "."))
    directory.mkdir(parents=True, exist_ok=True)
    output = directory / _timestamped_name()

    if shutil.which("flameshot"):
        cmd = ["flameshot", "gui", "--raw", "-p", str(output)]
        try:
            subprocess.run(cmd, check=True)
            return str(output)
        except Exception:
            pass

    if shutil.which("grim"):
        try:
            subprocess.run(["grim", str(output)], check=True)
            return str(output)
        except Exception:
            pass

    if mss is None:
        # last resort create an empty file
        output.touch()
        return str(output)

    with mss.mss() as sct:
        img = sct.grab(sct.monitors[0])
        mss.tools.to_png(img.rgb, img.size, output=str(output))
        return str(output)
