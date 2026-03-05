from lma.security import is_safe_command, sanitize_text


def test_command_allowed():
    cfg = {"security": {"allow_commands": ["ls", "cat"]}}
    assert is_safe_command("ls -l", cfg)
    assert not is_safe_command("rm -rf /", cfg)


def test_sanitize_text():
    dirty = "ls; rm -rf /"
    clean = sanitize_text(dirty)
    assert "rm" not in clean
