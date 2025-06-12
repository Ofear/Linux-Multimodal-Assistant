"""Audio transcription utilities."""

from __future__ import annotations

from typing import Optional

import shutil
import subprocess


def transcribe_audio(path: str) -> str:
    """Transcribe ``path`` using available backends."""

    try:
        from whispercpp import WhisperCPP

        model = WhisperCPP()
        return model.transcribe(path)
    except Exception:
        pass

    if shutil.which("whisper"):
        try:
            result = subprocess.check_output(["whisper", path, "--model", "base", "--output", "-"], text=True)
            return result.strip()
        except Exception:
            pass

    try:
        from faster_whisper import WhisperModel

        model = WhisperModel("base", device="cpu")
        segments, _ = model.transcribe(path)
        return " ".join(text for _, text in segments)
    except Exception:
        pass

    try:
        import speech_recognition as sr

        recognizer = sr.Recognizer()
        with sr.AudioFile(path) as source:
            audio = recognizer.record(source)
        return recognizer.recognize_sphinx(audio)
    except Exception:
        pass
    return ""
