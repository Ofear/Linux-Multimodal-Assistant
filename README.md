# Linux-Multimodal-Assistant

The **Linux Multimodal Assistant (LMA)** is a comprehensive AI-powered desktop assistant for Linux systems. It provides voice-controlled, visual, and text-based automation through hotkey-triggered workflows that capture audio, screenshots, and clipboard content to assist with various tasks using large language models.

## Key Features

### 🖥️ **Multimodal Input Processing**
- **Full Multimodal (Ctrl+Alt+A)**: Combines screenshot capture with voice input for context-aware assistance
- **Voice-Only (Ctrl+Alt+M)**: Pure voice commands without screen capture for general queries
- **Text Selection (Ctrl+Alt+V)**: Process selected text with voice commands (translate, summarize, etc.)

### 🎙️ **Advanced Voice Processing**
- Multiple transcription backends: whisper.cpp, faster-whisper, SpeechRecognition
- Offline speech recognition capabilities
- High-quality audio capture with sox/ffmpeg fallbacks

### 🔊 **Text-to-Speech (TTS)**
- Primary engine: Piper (high-quality neural TTS)
- Fallback: espeak for universal compatibility
- Configurable voices and speech settings

### 🔐 **Enterprise-Grade Security**
- Command whitelisting and sanitization
- Interactive confirmation dialogs for dangerous operations
- Sensitive data redaction in logs
- Shell injection prevention

### 🌐 **Flexible LLM Integration**
- OpenAI GPT-4o for vision-capable queries
- Local model support via Ollama (llava, mistral)
- Automatic model selection based on input type
- Robust retry logic and fallback mechanisms

### 🖱️ **System Integration**
- Mouse and keyboard automation
- Desktop notifications and dialogs
- Clipboard management
- Cross-platform compatibility (X11/Wayland)

## Installation

### 1. Clone and Setup
```bash
git clone https://github.com/yourname/Linux-Multimodal-Assistant.git
cd Linux-Multimodal-Assistant
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
# Install piper-tts separately due to dependency conflicts:
pip install piper-tts --no-deps piper-phonemize-fix onnxruntime numpy
```

### 3. Install System Dependencies
```bash
# Ubuntu/Debian
sudo apt install flameshot ffmpeg xdotool libnotify-bin zenity espeak

# Wayland users may need grim and ydotool instead of flameshot and xdotool
sudo apt install grim ydotool
```

### 4. Configure
Edit `config.json` in the project root:
- Set your `llm.openai_api_key` or configure local endpoint
- Adjust hotkeys if needed (defaults: Ctrl+Alt+A/M/V)
- Ensure `screenshot_dir` exists
- Configure TTS preferences

## Usage

### Launch the Assistant
```bash
python -m lma.assistant
```

You'll see a welcome message with available hotkeys. The assistant runs in the background listening for hotkey activation.

### Hotkey Workflows

#### **Ctrl+Alt+A - Full Multimodal**
Perfect for questions about screen content:
- "What's on this webpage?"
- "Summarize this document"
- "Help me understand this error message"

#### **Ctrl+Alt+M - Voice Only**
For general queries without screen context:
- "What's the weather today?"
- "Help me write an email"
- "Tell me a joke"

#### **Ctrl+Alt+V - Text Processing**
1. Select text in any application
2. Press Ctrl+Alt+V
3. Speak your command: "Translate to Spanish", "Fix grammar", "Summarize this"
4. The result replaces your clipboard content

### Configuration Options

The `config.json` file provides extensive customization:

```json
{
  "hotkeys": {
    "activate": "Ctrl+Alt+A",
    "voice_input": "Ctrl+Alt+M", 
    "text_selection": "Ctrl+Alt+V"
  },
  "llm": {
    "mode": "gpt-4o",
    "openai_api_key": "your-key-here",
    "local_endpoint": "http://localhost:11434"
  },
  "tts": {
    "enabled": true,
    "engine": "piper",
    "voice": "en_US-lessac-medium"
  },
  "security": {
    "allow_commands": ["ls", "cd", "chmod", "cat"],
    "confirm_required": ["sudo", "rm", "mv"]
  }
}
```

## Architecture

The assistant uses a modular architecture with specialized components:

- **`assistant.py`**: Main orchestrator with workflow-specific methods
- **`hotkey_listener.py`**: Global hotkey detection and dispatch
- **`mic_capture.py`**: Audio recording with multiple backends
- **`transcribe.py`**: Speech-to-text with offline capabilities
- **`screenshot.py`**: Screen capture for visual context
- **`llm_client.py`**: LLM communication and model selection
- **`notifier.py`**: TTS, notifications, and user dialogs
- **`security.py`**: Command validation and sanitization
- **`clipboard.py`**: System clipboard integration

## Development

### Running Tests
```bash
pytest
```

### Integration Testing
See `docs/INTEGRATION_TESTING.md` for comprehensive testing procedures covering all workflows and security features.

### Contributing
1. Fork the repository
2. Create a feature branch
3. Ensure tests pass
4. Submit a pull request

## System Requirements

- **OS**: Linux (X11 or Wayland)
- **Python**: 3.8+
- **Audio**: Working microphone and speakers
- **Display**: GUI environment for screenshots
- **Memory**: 2GB+ RAM (4GB+ recommended for local models)

## Troubleshooting

### Common Issues

**Audio not working**: Verify microphone permissions and test with `sox -d test.wav trim 0 5`

**Screenshots failing**: Install `flameshot` (X11) or `grim` (Wayland)

**Hotkeys not responding**: Check for conflicting applications using the same key combinations

**TTS not speaking**: Install `espeak` and verify audio output with `espeak "test"`

**Security dialogs missing**: Install `zenity` for confirmation dialogs

### Logs
Check `assistant.log` for detailed operation logs, error messages, and backend selection information.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## Roadmap

- [ ] Plugin system for extensible functionality
- [ ] Web interface for remote control
- [ ] Additional TTS engines and voices
- [ ] Advanced computer vision capabilities
- [ ] Integration with more local LLM providers

---

**Note**: This assistant is designed for productivity and automation. Always review and understand any suggested commands before execution, especially those requiring elevated privileges.
