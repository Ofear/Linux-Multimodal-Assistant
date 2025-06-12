from lma.security import is_command_allowed, sanitize_command


def test_command_allowed():
    cfg = {"security": {"allow_commands": ["ls", "cat"]}}
    assert is_command_allowed("ls -l", cfg)
    assert not is_command_allowed("rm -rf /", cfg)


def test_sanitize_command():
    dirty = "rm -rf /; echo hi"
    clean = sanitize_command(dirty)
    assert ";" not in clean
