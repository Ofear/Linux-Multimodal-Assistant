# Linux-Multimodal-Assistant

The **Linux Multimodal Assistant (LMA)** provides keyboard, mouse and voice
driven automation on Linux desktops. Hotkey triggered workflows capture audio
and screenshots, transcribe speech and send prompts to large language models to
assist with common tasks.

The repository now includes working implementations for audio capture,
transcription, screenshot handling and LLM communication.

## Installation

1. Clone the repository and create a Python virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `config.json` and adjust values to match your system.

## Configuration

The example `config.json` defines providers for the LLM, transcription and text
to speech subsystems.  Edit the `endpoint`, model names and other values as
needed.  You can also customise the hotkey used to activate the assistant
(default is `ctrl+alt+space`) and the directory where screenshots are stored.

## Usage and Key Features

Once configured, you can launch the assistant by running:

```bash
python -m lma.assistant
```

The assistant listens for the activation hotkey defined in your configuration
file. When triggered it captures audio from the microphone, transcribes your
request and sends it to the configured LLM. Screenshot capture, clipboard
management and basic mouse/keyboard control are also available.

## Contributing

1. Fork the repository and create a new branch for your change.
2. Install the dependencies and ensure that `pytest` runs successfully.
3. Submit a pull request describing your changes.

## Running Tests

After installing the dependencies you can run the automated test suite using:

```bash
pytest
```

Contributions should include corresponding tests whenever possible.

## License

This project is licensed under the [MIT License](LICENSE).
