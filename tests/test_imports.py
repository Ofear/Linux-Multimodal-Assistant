"""Ensure core modules are importable."""

import importlib

MODULES = [
    "lma.assistant",
    "lma.hotkey_listener",
    "lma.mic_capture",
    "lma.screenshot",
    "lma.transcribe",
    "lma.clipboard",
    "lma.llm_client",
    "lma.mouse_controller",
    "lma.keyboard_injector",
    "lma.notifier",
    "lma.security",
    "lma.utils",
]


def test_module_imports():
    for name in MODULES:
        module = importlib.import_module(name)
        assert module is not None
