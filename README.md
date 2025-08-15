# LLMShell

A command-line interface that translates natural language to system commands using LLM (Large Language Model).

## Features

- Natural language to system command translation
- Command existence validation
- Interactive command confirmation
- Rich terminal output with syntax highlighting
- Support for multiple LLM providers

## Installation

This project uses `uv` for dependency management. Make sure you have `uv` installed:

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then install the project:

```bash
# Clone the repository
git clone <your-repo-url>
cd llmshell

# Install dependencies
uv sync

# Install the package in development mode
uv pip install -e .
```

## Usage

The CLI uses `?` as the command symbol:

```bash
# Basic usage
? show network ip

# More complex commands
? find all files larger than 100MB in current directory
? check system memory usage
? list running processes
```

## Configuration

LLMShell uses a configuration file located at `~/.llmshell.config`. You can manage your configuration using the built-in commands:

### Set your API key:
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

### View current configuration:
```bash
llmshell config show
```

### Edit configuration file:
```bash
llmshell config edit
```

### Get specific configuration value:
```bash
llmshell config get llm.openai.model
```

### Set LLM provider:
```bash
llmshell config provider deepseek
```

### List available providers:
```bash
llmshell config list-providers
```

### Available Configuration Options:

#### LLM Providers
- `llm.provider`: Current LLM provider (openai, deepseek, doubao, qwen)
- `llm.openai.*`: OpenAI settings (api_key, model, temperature, base_url)
- `llm.deepseek.*`: DeepSeek settings (api_key, model, temperature, base_url)
- `llm.doubao.*`: Doubao settings (api_key, model, temperature, base_url)
- `llm.qwen.*`: Qwen settings (api_key, model, temperature, base_url)

#### UI Settings
- `ui.theme`: Terminal theme (default: monokai)
- `ui.max_output_lines`: Maximum lines to show (default: 50)
- `ui.show_confirmations`: Show command confirmations (default: true)

#### Safety Settings
- `safety.enable_sanitization`: Enable command sanitization (default: true)
- `safety.timeout_seconds`: Command timeout (default: 30)

### Backward Compatibility

For backward compatibility, the system will also check for environment variables:
- `OPENAI_API_KEY` for OpenAI
- `DEEPSEEK_API_KEY` for DeepSeek
- `DOUBAO_API_KEY` for Doubao
- `QWEN_API_KEY` for Qwen

## Development

```bash
# Install development dependencies
uv sync --extra dev

# Run tests
uv run pytest

# Format code
uv run black .
uv run isort .

# Lint code
uv run flake8
```

## How it works

1. User inputs natural language command (e.g., "show network ip")
2. LLM translates it to possible system commands
3. System validates command existence
4. User confirms execution
5. Command is executed and output is displayed

## License

MIT License - see LICENSE file for details.
