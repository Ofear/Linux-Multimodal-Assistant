from lma.transcribe import transcribe_audio


def test_transcribe_returns_string(tmp_path):
    wav = tmp_path / "sample.wav"
    wav.write_bytes(b"RIFF0000WAVEfmt ")
    result = transcribe_audio(str(wav))
    assert isinstance(result, str)
