# Text Autocomplete - AI-Powered Text Editor

A Python-based TUI (Text User Interface) text editor with real-time AI-powered word autocompletion, similar to GitHub Copilot but for natural language text.

## Features

- **Real-time AI Autocomplete**: As you type, the system predicts the next few words or phrases
- **Ghost Text Display**: Suggestions appear in a faint style before the cursor
- **Easy Acceptance**: Press Tab or Right Arrow to accept suggestions
- **Smart Refresh**: Suggestions update automatically as you type
- **Nano-like Interface**: Familiar text editor controls
- **File Operations**: Save and load text files
- **Customizable AI Backend**: Configure your own OpenAI-compatible endpoint

## Installation

1. Clone the repository:
```bash
git clone https://github.com/eli32-vlc/text-autocomplete.git
cd text-autocomplete
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your API settings:
```bash
cp config.example.json config.json
```

Edit `config.json` with your API details:
```json
{
  "api_endpoint": "https://api.openai.com/v1",
  "api_key": "your-api-key-here",
  "model": "gpt-4",
  "max_tokens": 30,
  "temperature": 0.7,
  "pause_delay_ms": 200
}
```

## Usage

### Start the editor

```bash
python text_autocomplete.py
```

### Open an existing file

```bash
python text_autocomplete.py filename.txt
```

## Keyboard Controls

- **Arrow Keys**: Move cursor
- **Tab / Right Arrow**: Accept AI suggestion
- **Ctrl+S**: Save file
- **Ctrl+O**: Open file
- **Ctrl+X**: Exit
- **Ctrl+G**: Toggle AI autocomplete on/off

## How It Works

1. **Type Naturally**: Start typing your text
2. **Pause Briefly**: After a short pause (default 200ms), the AI generates suggestions
3. **See Suggestions**: Ghost text appears showing the predicted continuation
4. **Accept or Continue**: Press Tab to accept, or keep typing to refine
5. **Smart Matching**: If your typing matches the suggestion, it stays; otherwise it refreshes

## Configuration Options

- `api_endpoint`: Your OpenAI-compatible API endpoint
- `api_key`: Your API key
- `model`: Model to use (e.g., "gpt-4", "gpt-3.5-turbo")
- `max_tokens`: Maximum tokens for completion (controls suggestion length)
- `temperature`: Creativity of suggestions (0.0-1.0)
- `pause_delay_ms`: Milliseconds to wait before requesting suggestions

## Requirements

- Python 3.7+
- Terminal with curses support (Linux/macOS native, Windows requires windows-curses)
- OpenAI API key or compatible endpoint

## License

MIT License
