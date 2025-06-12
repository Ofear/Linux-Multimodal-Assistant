# Integration Testing Guide

This document outlines how to run full end-to-end tests of the Linux Multimodal Assistant on a desktop with working audio and screenshot tools.

## Prerequisites

* A Linux system with a functioning microphone and GUI environment.
* Dependencies installed from `requirements.txt`.
* External tools: `flameshot` or `grim` for screenshots, `ffmpeg` or `sox` for audio recording, `xdotool` or `ydotool` for mouse and keyboard control, and `notify-send`/`zenity` for notifications.
* `openai` API key or a running local LLM as defined in `config.json`.

## 1. Clone and Configure

1. Clone this repository and enter the directory:
   ```bash
   git clone https://github.com/yourname/Linux-Multimodal-Assistant.git
   cd Linux-Multimodal-Assistant
   ```
2. Create a virtual environment and install Python dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Copy `config.json` and update the following fields:
   - `llm.openai_api_key` with your key or configure `local_endpoint`.
   - Adjust hotkeys if needed.
   - Ensure `screenshot_dir` exists.

## 2. Verify External Tools

Check that required tools are available. Install them with your package manager if missing:
```bash
which flameshot ffmpeg xdotool notify-send || sudo apt install flameshot ffmpeg xdotool libnotify-bin
```
Wayland users may need `grim` and `ydotool` instead.

## 3. Run Unit Tests

Before running integration tests, ensure the unit tests pass:
```bash
pytest
```
All tests should report `PASSED`.

## 4. Launch the Assistant

Start the assistant in one terminal:
```bash
python -m lma.assistant
```
A log file `assistant.log` will be created in the project root. Leave this terminal running during the tests.

## 5. Integration Test Scenarios

Perform the following manual tests. Results should be visible either via desktop notifications or spoken aloud depending on your configuration.

1. **Hotkey Capture**
   - Press the activation hotkey (default `Ctrl+Alt+A`).
   - Speak a short request (e.g., "What\'s the weather today?").
   - A screenshot should be taken and audio recorded. The LLM response appears on screen or through TTS.
2. **Mic‑Only Command**
   - Press `Ctrl+Alt+M` and issue a voice command. Verify that the transcription appears and the response is displayed.
3. **Text Selection Assist**
   - Select some text in another application.
   - Press `Ctrl+Alt+V` and provide a prompt to transform or translate the text. The clipboard should be replaced with the response.
4. **Mouse and Keyboard Automation**
   - Trigger a command from the LLM that clicks or types. Confirm that the action happens at the expected screen coordinates.
5. **Security Confirmation**
   - Ask the assistant to run a restricted command like `rm`. Ensure a confirmation dialog appears before execution.

## 6. Review Logs

Check `assistant.log` for entries showing:
- Successful screenshot capture with resolution and filename.
- Audio recording and transcription backend used.
- LLM request and truncated response.
- Any errors during the test runs.
Log rotation should create new files if the size exceeds 10MB.

## 7. Troubleshooting

If audio capture fails, verify microphone permissions and that `ffmpeg` or `sox` can record manually. Screenshot issues may be resolved by installing `flameshot` or using the `grim` fallback on Wayland. Consult the log file for details on which backends were attempted.

## 8. Finish

Once the above tests pass, you have confirmed the assistant works end-to-end on your system. You can optionally package it with PyInstaller or create a systemd service as described in the README.
