📄 Product Requirements Document (PRD)
Project: Linux Multimodal Assistant
Target Developer: OpenAI Codex

🔥 Objective
Develop a Linux-native multimodal AI assistant, that can:
Capture and understand screen content


Transcribe and respond to voice commands


Interact with selected or clipboard text


Query an LLM (GPT-4o or local models)


Control mouse and keyboard


Provide spoken or visual responses


All components must run reliably on X11 and Wayland, support custom hotkeys, operate offline where possible, and prioritize safety and performance.

✅ Key Features
1. 🖥️ Screen Vision
Triggered via hotkey (e.g., Ctrl+Alt+A)


Capture full or partial screen using:


flameshot (GUI area selection)


grim (Wayland alternative)


Send screenshot to LLM (vision-capable)


Optional: compress image (JPEG quality 80%)


2. 🎙️ Voice Input
Triggered via hotkey (e.g., Ctrl+Alt+M)


Record 5–10 seconds of mic input using:


Preferred: sox


Fallback: ffmpeg


Transcribe with:


whisper.cpp (offline)


faster-whisper (Python alternative)


Output used as prompt to LLM


3. 📋 Text Selection Input
Triggered via hotkey (e.g., Ctrl+Alt+V)


Capture selected or clipboard text via:


xclip (X11)


wl-paste (Wayland)


Combine with a spoken or typed command


4. 🧠 AI Query System
Query either:


GPT-4o (OpenAI API, for vision + reasoning)


Ollama local models (e.g., llava, mistral)


Dynamically select model based on:


Vision input → GPT-4o or llava


Text input → mistral or GPT-4o


Use async HTTP (httpx) with retry logic (max 3)


Sanitize responses (remove shell injection patterns)


5. 🖱️ Mouse + Keyboard Control
Simulate mouse movement and clicks via:


xdotool (X11)


ydotool (Wayland, must run as root)


pyautogui as fallback


Simulate typing or command injection


Validate all coordinates and commands before execution


6. 🔈 Output / Feedback
Display result using:


notify-send (non-blocking)


zenity (dialogs for confirmation, error, input)


Optional: Speak response with:


Preferred: piper


Fallbacks: espeak, gTTS


Configurable verbosity via config.json


7. 🔐 Security & Safety
Whitelist only safe commands (e.g., ls, chmod)


Prompt for confirmation before:


Any command containing rm, sudo, mv


Sanitize LLM output to prevent code injection


Redact sensitive logs (API keys, clipboard contents)


8. 🔁 Custom Hotkeys & Config
All hotkeys should be editable in config.json


Use evdev or keyboard Python library for keybinding


Fallback-safe defaults: Ctrl+Alt+A / M / V



📦 Folder Structure
linux-multimodal-assistant/
├── assistant.py               # Main orchestrator
├── config.json                # User config (hotkeys, models, etc)
├── hotkey_listener.py         # Global hotkey bindings
├── mic_capture.py             # Records audio
├── screenshot.py              # Captures screen
├── transcribe.py              # Runs whisper locally
├── clipboard.py               # Reads text selection or clipboard
├── llm_client.py              # Routes to GPT-4o or local models
├── mouse_controller.py        # Simulates mouse input
├── keyboard_injector.py       # Simulates typing
├── notifier.py                # Popup, TTS, or notifications
├── security.py                # Whitelist & sanitization logic
├── utils.py                   # Env detection, image compression, etc
├── assistant.log              # Rotating logs
├── requirements.txt
├── README.md
└── tests/                     # Unit and integration tests


⚙️ Config Schema (config.json)
{
  "hotkeys": {
    "activate": "Ctrl+Alt+A",
    "voice_input": "Ctrl+Alt+M",
    "text_selection": "Ctrl+Alt+V",
    "allow_custom": true
  },
  "llm": {
    "mode": "gpt-4o",
    "openai_api_key": "sk-xxx",
    "local_endpoint": "http://localhost:11434",
    "primary_local_model": "llava",
    "fallback_model": "mistral"
  },
  "tts": {
    "enabled": true,
    "engine": "piper",
    "fallback": "espeak",
    "voice": "en_US-lessac-medium"
  },
  "security": {
    "allow_commands": ["ls", "cd", "chmod", "cat"],
    "confirm_required": ["sudo", "rm", "mv"],
    "sanitize_inputs": true
  },
  "logging": {
    "level": "INFO",
    "redact_sensitive": true,
    "max_size_mb": 10
  }
}


🧪 Testing Plan
Unit Tests (in tests/):
test_transcribe.py: mock mic input, return dummy transcript


test_llm_client.py: mock GPT and local calls, validate routing


test_screenshot.py: mock file creation + format validation


test_security.py: validate command sanitization + whitelisting


Integration Tests:
Simulate hotkey → screenshot → voice → LLM → mouse click


Simulate selection → translation → clipboard replacement


Ensure fallback from GPT-4o to local works on API fail


Edge Cases:
No internet → local fallback


Invalid coordinates → discard click


Mic error → prompt for manual text


Wrong button clicked → confirm retry



📌 Deployment
Package using PyInstaller


Provide .deb and .rpm for installation


Auto-start via systemd user service


Optional: run from tray with PyQt5 button



✅ Codex Instructions
Implement the assistant as defined in this PRD. Use assistant.py as the orchestrator and connect modular components as described. Prioritize X11 and Wayland support, model fallback logic, command safety, logging, and ease of configuration. Use the config and folder structure verbatim. No additional design input is needed — this is the final blueprint.

📞 Questions
Codex should not require further clarification. All API keys, model preferences, command safety rules, UI styles, and dependencies are defined. If any external binary (e.g., xdotool, flameshot) is missing, log and skip with fallback.