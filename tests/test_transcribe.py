from lma.transcribe import transcribe_audio


def test_transcribe_returns_dummy(tmp_path):
    wav = tmp_path / "sample.wav"
    wav.write_bytes(b"RIFF0000WAVEfmt ")
    result = transcribe_audio(str(wav))
    assert result == "dummy transcript"
