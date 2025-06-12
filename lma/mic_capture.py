"""Microphone audio capture utilities."""

from __future__ import annotations

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

    try:
        import sounddevice as sd  # imported lazily for optional dependency
        import soundfile as sf

        data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=channels)
        sd.wait()
    except Exception:
        return None

    path = tempfile.mkstemp(suffix=".wav")[1]
    sf.write(path, data, samplerate)
    return path
