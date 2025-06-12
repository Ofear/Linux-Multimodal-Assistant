from pathlib import Path

from lma.screenshot import take_screenshot


def test_take_screenshot_creates_file(tmp_path, monkeypatch):
    cfg = {"screenshot_dir": str(tmp_path)}

    def fake_run(*args, **kwargs):
        raise FileNotFoundError

    monkeypatch.setattr("subprocess.run", fake_run)
    path = take_screenshot(cfg)
    assert Path(path).exists()
    assert path.endswith(".png")
