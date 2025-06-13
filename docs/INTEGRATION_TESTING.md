# Integration Testing Guide

This document outlines how to run full end-to-end tests of the Linux Multimodal Assistant on a desktop with working audio and screenshot tools.

## Prerequisites

* A Linux system with a functioning microphone and GUI environment.
* Dependencies installed from `requirements.txt`.
* External tools: `flameshot` or `grim` for screenshots, `ffmpeg` or `sox` for audio recording, `xdotool` or `ydotool` for mouse and keyboard control, `notify-send`/`zenity` for notifications, and `espeak` for TTS fallback.
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
   # Install piper-tts separately due to dependency conflicts:
   pip install piper-tts --no-deps piper-phonemize-fix onnxruntime numpy
   ```
3. Rename the existing `config.example.json` to `config.json` file in the project root and update the following fields:
   - `llm.openai_api_key` with your key or configure `local_endpoint`.
   - Adjust hotkeys if needed.
   - Ensure `screenshot_dir` exists (create the directory if it doesn't exist).

## 2. Verify External Tools

Check that required tools are available. Install them with your package manager if missing:
```bash
which flameshot ffmpeg xdotool notify-send zenity espeak || sudo apt install flameshot ffmpeg xdotool libnotify-bin zenity espeak
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
A log file `assistant.log` will be created in the project root. Leave this terminal running during the tests. You should see a welcome message listing the available hotkeys.

## 5. Integration Test Scenarios

Perform the following manual tests. Results should be visible either via desktop notifications, spoken aloud (if TTS is enabled), or through dialogs depending on your configuration.

### 5.1 Full Multimodal Input (Ctrl+Alt+A)
- Press the activation hotkey (default `Ctrl+Alt+A`).
- A screenshot should be captured automatically.
- Speak a request that references the screen content (e.g., "What's in this window?", "Summarize this webpage").
- Verify that both screenshot and audio are processed.
- The LLM response should reference visual elements and be displayed/spoken.

### 5.2 Voice-Only Input (Ctrl+Alt+M)
- Press `Ctrl+Alt+M` and issue a voice command that doesn't require screen context.
- Examples: "What's the weather today?", "Tell me a joke", "Help me write an email".
- Verify that NO screenshot is taken (check logs).
- The response should be displayed/spoken.

### 5.3 Text Selection Processing (Ctrl+Alt+V)
- Select some text in another application (browser, text editor, etc.).
- Press `Ctrl+Alt+V`.
- You should see a notification saying "Selected text captured. Please provide a voice command..."
- Speak a command to transform the text (e.g., "Translate to Spanish", "Summarize this", "Fix grammar").
- The processed result should replace the original text in your clipboard.
- Paste somewhere to verify the clipboard was updated.

### 5.4 Security Features
- Try asking the assistant to run a dangerous command like "delete all files" or "sudo rm -rf /".
- If the LLM suggests dangerous commands, you should see:
  - Warning logs about unsafe commands
  - Confirmation dialogs (zenity) asking for permission
  - Commands should not execute without explicit confirmation

### 5.5 TTS (Text-to-Speech) Testing
- Ensure `tts.enabled` is `true` in your config.
- Trigger any assistant action and verify responses are spoken aloud.
- Check logs for TTS backend used (piper or espeak fallback).

### 5.6 Mouse and Keyboard Automation
**⚠️ Important**: Test these in a safe environment as they will actually control your mouse and keyboard.

#### Mouse Control Tests
- Open a text editor or simple application.
- Ask the assistant: "Click at coordinates 500, 300" or "Move mouse to 400, 200".
- Verify the mouse moves to the specified coordinates.
- Try: "Click at (100, 100) and then move to (200, 200)".
- Check logs for coordinate validation and execution confirmation.

#### Keyboard Automation Tests
- Focus on a text input field.
- Ask the assistant: "Type text 'Hello World'" or "Enter text: This is a test".
- Verify the text appears in the focused field.
- Try hotkey commands: "Press ctrl+a" or "Send hotkey alt+tab".
- Check that keyboard shortcuts work as expected.

#### Automation Safety Tests
- Try asking for automation outside screen bounds: "Click at 5000, 5000".
- Verify the assistant rejects invalid coordinates with warning logs.
- Test automation commands mixed with normal responses.

### 5.7 Command Execution
**⚠️ Important**: Only test with safe commands from your allowed list.

- Ensure your `config.json` has safe commands in `security.allow_commands` like `["ls", "cd", "pwd", "date"]`.
- Ask the assistant: "List files in current directory" or "What's the current date?".
- If the LLM suggests using `ls` or `date`, it should execute and show results.
- Try asking for a dangerous command like "Delete all files" - it should be blocked or require confirmation.
- Check logs for command extraction, validation, and execution status.

## 6. Review Logs

Check `assistant.log` for entries showing:
- Successful screenshot capture with resolution and filename.
- Audio recording and transcription backend used.
- LLM request and truncated response (with sensitive data redacted).
- Different workflow types being processed correctly.
- TTS engine selection and usage.
- Security checks and command validation.
- Mouse/keyboard automation commands and coordinate validation.
- Shell command execution with output and status.
- Any errors during the test runs.
Log rotation should create new files if the size exceeds 10MB.

## 7. Troubleshooting

### Audio Issues
If audio capture fails, verify microphone permissions and that `ffmpeg` or `sox` can record manually:
```bash
# Test with sox
sox -d test_recording.wav trim 0 5

# Test with ffmpeg
ffmpeg -f alsa -i default -t 5 test_recording.wav
```

### Screenshot Issues
Screenshot problems may be resolved by installing `flameshot` or using the `grim` fallback on Wayland. Check which backend is being used in the logs.

### TTS Issues
If speech output isn't working:
- Verify espeak is installed: `espeak "test"`
- Check audio output devices: `pactl list short sinks`
- For piper, ensure the voice model is available

### Security Dialogs
If zenity dialogs don't appear:
- Install zenity: `sudo apt install zenity`
- Test manually: `zenity --question --text "Test question"`

### Hotkey Issues
If hotkeys aren't working:
- Check if pynput is properly installed
- Verify no other applications are using the same key combinations
- Try running with different desktop environments

### Automation Issues
If mouse/keyboard automation isn't working:
- **X11**: Ensure xdotool is installed: `sudo apt install xdotool`
- **Wayland**: Install ydotool and ensure it has proper permissions: `sudo apt install ydotool`
- **PyAutoGUI fallback**: Verify it can control your desktop: `python3 -c "import pyautogui; pyautogui.click()"`
- Check logs for which automation backend is being used

### Command Execution Issues
If shell commands aren't executing:
- Verify commands are in the `security.allow_commands` list in config.json
- Check that dangerous commands are properly blocked
- Ensure subprocess execution has proper permissions
- Review logs for command validation and execution status

Consult the log file for details on which backends were attempted and any error messages.

## 8. Finish

Once the above tests pass, you have confirmed the assistant works end-to-end on your system with full workflow differentiation, TTS, security features, and complete automation capabilities. You can optionally package it with PyInstaller or create a systemd service as described in the README.
