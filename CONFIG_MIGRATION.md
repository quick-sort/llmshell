# Configuration Migration Guide

## Overview

LLMShell has been updated to use a centralized configuration system stored in `~/.llmshell.config` instead of environment variables and `.env` files.

## What Changed

### Before (Old System)
- Configuration via environment variables (`OPENAI_API_KEY`, etc.)
- `.env` file support
- Hard-coded defaults in code

### After (New System)
- Configuration file at `~/.llmshell.config`
- Built-in configuration management commands
- Configurable settings for UI, safety, and LLM parameters
- Backward compatibility with environment variables

## Migration Steps

### 1. For New Users
```bash
# Install dependencies
uv sync

# Set your API key
llmshell config set openai.api_key "your-api-key-here"

# Start using LLMShell
uv run python run.py
```

### 2. For Existing Users
If you were using environment variables or `.env` files:

1. **Your existing setup will continue to work** - the system checks for `OPENAI_API_KEY` environment variable as a fallback
2. **To migrate to the new system:**
   ```bash
   # Set your API key in the new config system
   llmshell config set openai.api_key "your-api-key-here"
   
   # Remove old .env file (optional)
   rm .env
   ```

## New Configuration Features

### Configuration Management Commands
```bash
# View current configuration
llmshell config show

# Set configuration values
llmshell config set openai.model gpt-4
llmshell config set ui.theme dracula
llmshell config set safety.timeout_seconds 60

# Get specific values
llmshell config get openai.model

# Edit configuration file directly
llmshell config edit
```

### Available Configuration Options

#### OpenAI Settings
- `openai.api_key`: Your OpenAI API key
- `openai.model`: Model to use (default: gpt-3.5-turbo)
- `openai.temperature`: Generation temperature (default: 0.1)

#### UI Settings
- `ui.theme`: Terminal theme (default: monokai)
- `ui.max_output_lines`: Maximum lines to show (default: 50)
- `ui.show_confirmations`: Show command confirmations (default: true)

#### Safety Settings
- `safety.enable_sanitization`: Enable command sanitization (default: true)
- `safety.timeout_seconds`: Command timeout (default: 30)

## Configuration File Format

The configuration file is stored as JSON at `~/.llmshell.config`:

```json
{
  "openai": {
    "api_key": "your-api-key-here",
    "model": "gpt-3.5-turbo",
    "temperature": 0.1
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

## Benefits of the New System

1. **Centralized Configuration**: All settings in one place
2. **Easy Management**: Built-in commands for viewing and editing
3. **User-Specific**: Configuration is per-user, not per-project
4. **Extensible**: Easy to add new configuration options
5. **Backward Compatible**: Still works with environment variables
6. **Secure**: API keys are stored securely in user's home directory

## Troubleshooting

### Configuration File Issues
```bash
# If config file is corrupted, remove it to reset to defaults
rm ~/.llmshell.config

# The system will recreate it with default values on next run
```

### Permission Issues
```bash
# If you can't write to ~/.llmshell.config
chmod 600 ~/.llmshell.config
```

### Backward Compatibility
The system will automatically use environment variables if the configuration file doesn't exist or if the API key is not set in the config file.
