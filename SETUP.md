# LLMShell Setup Guide

## Quick Start

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Set up your API key:**
   ```bash
   # For OpenAI
   llmshell config api-key "your-openai-api-key-here" --provider openai
   
   # For DeepSeek
   llmshell config api-key "your-deepseek-api-key-here" --provider deepseek
   
   # For Doubao
   llmshell config api-key "your-doubao-api-key-here" --provider doubao
   
   # For Qwen
   llmshell config api-key "your-qwen-api-key-here" --provider qwen
   ```

3. **Run the interactive shell:**
   ```bash
   uv run python run.py
   ```

## Usage Examples

### Interactive Mode
```bash
$ uv run python run.py
LLMShell - Natural language to system commands
Type 'exit' or 'quit' to exit, 'help' for help

? show network ip
? check system memory
? find large files
? exit
```

### Command Line Mode
```bash
# Single command
uv run python -m llmshell.cli "show network ip"

# With options
uv run python -m llmshell.cli --model gpt-4 --force "check disk space"
```

### Using the '?' Command (after setup)
```bash
# Create symlink (requires sudo)
sudo make install-symlink

# Then use '?' from anywhere
? show network ip
? check system memory
```

## Project Structure

```
llmshell/
├── llmshell/           # Main package
│   ├── __init__.py     # Package initialization
│   ├── cli.py          # Command-line interface
│   ├── core.py         # Core functionality
│   ├── llm.py          # LLM translation
│   └── utils.py        # Utility functions
├── tests/              # Test files
├── pyproject.toml      # Project configuration
├── run.py              # Simple entry point
├── llmshell.sh         # Shell script wrapper
├── Makefile            # Build automation
└── README.md           # Project documentation
```

## Configuration

### Configuration Options

#### LLM Providers
- `llm.provider`: Current LLM provider (openai, deepseek, doubao, qwen)
- `llm.openai.*`: OpenAI settings (api_key, model, temperature, base_url)
- `llm.deepseek.*`: DeepSeek settings (api_key, model, temperature, base_url)
- `llm.doubao.*`: Doubao settings (api_key, model, temperature, base_url)
- `llm.qwen.*`: Qwen settings (api_key, model, temperature, base_url)

#### UI Settings
- `ui.theme`: Terminal theme (default: monokai)
- `ui.max_output_lines`: Maximum output lines (default: 50)
- `ui.show_confirmations`: Show confirmations (default: true)

#### Safety Settings
- `safety.enable_sanitization`: Enable sanitization (default: true)
- `safety.timeout_seconds`: Command timeout (default: 30)

### Configuration File
The configuration is stored in `~/.llmshell.config`. You can manage it using:

```bash
# Set your API key
llmshell config set openai.api_key "your-api-key-here"

# View current config
llmshell config show

# Edit config file
llmshell config edit
```

Example configuration:
```json
{
  "llm": {
    "provider": "openai",
    "openai": {
      "api_key": "your-openai-api-key-here",
      "model": "gpt-3.5-turbo",
      "temperature": 0.1,
      "base_url": "https://api.openai.com/v1"
    },
    "deepseek": {
      "api_key": "your-deepseek-api-key-here",
      "model": "deepseek-chat",
      "temperature": 0.1,
      "base_url": "https://api.deepseek.com/v1"
    },
    "doubao": {
      "api_key": "your-doubao-api-key-here",
      "model": "doubao-pro",
      "temperature": 0.1,
      "base_url": "https://api.doubao.com/v1"
    },
    "qwen": {
      "api_key": "your-qwen-api-key-here",
      "model": "qwen-turbo",
      "temperature": 0.1,
      "base_url": "https://dashscope.aliyuncs.com/api/v1"
    }
  },
  "ui": {
    "theme": "monokai",
    "max_output_lines": 50,
    "show_confirmations": true
  },
  "safety": {
    "enable_sanitization": true,
    "timeout_seconds": 30
  }
}
```

## Development

### Install Development Dependencies
```bash
uv sync --extra dev
```

### Run Tests
```bash
uv run pytest tests/ -v
```

### Format Code
```bash
uv run black llmshell/ tests/
uv run isort llmshell/ tests/
```

### Lint Code
```bash
uv run flake8 llmshell/ tests/
```

### Run Demo
```bash
uv run python demo.py
```

## Features

- **Natural Language Translation**: Converts natural language to system commands
- **Command Validation**: Checks if commands exist in the system
- **Interactive Mode**: Continuous command processing with '?' prompt
- **Rich Output**: Beautiful terminal output with syntax highlighting
- **Safety Features**: Basic command sanitization
- **Fallback System**: Works even without API key using predefined mappings

## Troubleshooting

### Common Issues

1. **"No module named 'llmshell'"**
   - Make sure you're in the project directory
   - Run `uv sync` to install dependencies

2. **"API key not found in configuration"**
   - Set your API key: `llmshell config api-key "your-key" --provider <provider>`
   - Or edit the config: `llmshell config edit`

3. **"Command not found"**
   - The system will show which commands are available
   - Try different natural language descriptions

### Getting Help
- Use `help` or `?` in interactive mode
- Check the README.md for more information
- Run tests to verify installation: `uv run pytest tests/`

## Security Notes

- The system includes basic command sanitization
- Always review commands before execution
- Be careful with system-level commands
- The system will warn about dangerous patterns
