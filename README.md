# Linux-Multimodal-Assistant

The **Linux Multimodal Assistant (LMA)** aims to provide keyboard, mouse and
voice driven automation on Linux desktops.  It combines hotkey triggered
workflows with speech transcription and large language model (LLM) prompts to
help you perform repetitive tasks more quickly.

While most modules are currently placeholders, the configuration files and test
suite lay the groundwork for future development.

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

Once configured, you can experiment with the placeholder assistant by running:

```bash
python -m lma.assistant
```

The assistant will listen for the activation hotkey defined in your
configuration file.  When triggered it will eventually capture audio from the
microphone, transcribe your request and send it to the configured LLM.  Current
implementations simply return placeholders, but the structure is in place for
future automation including typing, clipboard actions and screenshot capture.

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
