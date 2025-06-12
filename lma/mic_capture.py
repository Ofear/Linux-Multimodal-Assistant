"""Microphone audio capture utilities."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from typing import Optional


def record_audio(duration: int = 5, samplerate: int = 16000, channels: int = 1) -> Optional[str]:
    """Record audio from the default microphone.

    Parameters
    ----------
    duration:
        Number of seconds to record.
    samplerate:
        Target sample rate.
    channels:
        Number of audio channels.

    Returns
    -------
    str or None
        Path to the recorded WAV file or ``None`` on failure.
    """

    path = tempfile.mkstemp(suffix=".wav")[1]

    try:
        import sounddevice as sd  # imported lazily for optional dependency
        import soundfile as sf

        data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=channels)
        sd.wait()
        sf.write(path, data, samplerate)
        return path
    except Exception:
        pass

    if shutil.which("sox"):
        cmd = [
            "sox",
            "-d",
            "-c",
            str(channels),
            "-r",
            str(samplerate),
            path,
            "trim",
            "0",
            str(duration),
        ]
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return path
        except Exception:
            pass

    if shutil.which("ffmpeg"):
        cmd = [
            "ffmpeg",
            "-y",
            "-f",
            "alsa",
            "-i",
            "default",
            "-t",
            str(duration),
            "-ac",
            str(channels),
            "-ar",
            str(samplerate),
            path,
        ]
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return path
        except Exception:
            pass

    return None
