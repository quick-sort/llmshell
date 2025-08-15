# Multi-Provider LLM Support Guide

## Overview

LLMShell now supports multiple LLM providers, allowing you to choose between different AI services for command translation. Supported providers include:

- **OpenAI** (GPT models)
- **DeepSeek** (DeepSeek Chat models)
- **Doubao** (Doubao Pro models)
- **Qwen** (Qwen models)

## Quick Start

### 1. Set Your Provider
```bash
# Choose your preferred provider
llmshell config provider openai
llmshell config provider deepseek
llmshell config provider doubao
llmshell config provider qwen
```

### 2. Set Your API Key
```bash
# Set API key for the current provider
llmshell config api-key "your-api-key-here"

# Or specify a provider
llmshell config api-key "your-api-key-here" --provider openai
```

### 3. Start Using LLMShell
```bash
uv run python run.py
```

## Provider Configuration

### OpenAI
```bash
# Set OpenAI as provider
llmshell config provider openai

# Set OpenAI API key
llmshell config api-key "sk-..." --provider openai

# Configure OpenAI settings
llmshell config set llm.openai.model "gpt-4"
llmshell config set llm.openai.temperature 0.1
```

**Default Settings:**
- Model: `gpt-3.5-turbo`
- Base URL: `https://api.openai.com/v1`
- Environment Variable: `OPENAI_API_KEY`

### DeepSeek
```bash
# Set DeepSeek as provider
llmshell config provider deepseek

# Set DeepSeek API key
llmshell config api-key "sk-..." --provider deepseek

# Configure DeepSeek settings
llmshell config set llm.deepseek.model "deepseek-chat"
llmshell config set llm.deepseek.temperature 0.1
```

**Default Settings:**
- Model: `deepseek-chat`
- Base URL: `https://api.deepseek.com/v1`
- Environment Variable: `DEEPSEEK_API_KEY`

### Doubao
```bash
# Set Doubao as provider
llmshell config provider doubao

# Set Doubao API key
llmshell config api-key "your-api-key" --provider doubao

# Configure Doubao settings
llmshell config set llm.doubao.model "doubao-pro"
llmshell config set llm.doubao.temperature 0.1
```

**Default Settings:**
- Model: `doubao-pro`
- Base URL: `https://api.doubao.com/v1`
- Environment Variable: `DOUBAO_API_KEY`

### Qwen
```bash
# Set Qwen as provider
llmshell config provider qwen

# Set Qwen API key
llmshell config api-key "your-api-key" --provider qwen

# Configure Qwen settings
llmshell config set llm.qwen.model "qwen-turbo"
llmshell config set llm.qwen.temperature 0.1
```

**Default Settings:**
- Model: `qwen-turbo`
- Base URL: `https://dashscope.aliyuncs.com/api/v1`
- Environment Variable: `QWEN_API_KEY`

## Configuration Management

### View Current Configuration
```bash
# Show all configuration
llmshell config show

# Show current provider
llmshell config get llm.provider
```

### List All Providers
```bash
# List providers and their status
llmshell config list-providers
```

### Switch Between Providers
```bash
# Switch to a different provider
llmshell config provider deepseek

# Verify the change
llmshell config get llm.provider
```

### Set Multiple API Keys
```bash
# Configure multiple providers
llmshell config api-key "openai-key" --provider openai
llmshell config api-key "deepseek-key" --provider deepseek
llmshell config api-key "doubao-key" --provider doubao
llmshell config api-key "qwen-key" --provider qwen
```

## Command Line Usage

### Specify Provider at Runtime
```bash
# Use a specific provider for one command
uv run python -m llmshell.cli --provider deepseek "show network ip"

# Use a specific provider with custom model
uv run python -m llmshell.cli --provider openai --model gpt-4 "check system memory"
```

### Interactive Mode with Provider
```bash
# Start interactive mode with specific provider
uv run python -m llmshell.cli --provider qwen
```

## Environment Variables

For backward compatibility, you can also set API keys using environment variables:

```bash
# Set environment variables
export OPENAI_API_KEY="sk-..."
export DEEPSEEK_API_KEY="sk-..."
export DOUBAO_API_KEY="your-key"
export QWEN_API_KEY="your-key"

# LLMShell will automatically detect and use the appropriate key
```

## Provider Comparison

| Provider | Default Model | Base URL | Pros | Cons |
|----------|---------------|----------|------|------|
| OpenAI | gpt-3.5-turbo | api.openai.com | Widely supported, reliable | Higher cost |
| DeepSeek | deepseek-chat | api.deepseek.com | Good performance, competitive pricing | Newer service |
| Doubao | doubao-pro | api.doubao.com | Chinese language support | Limited documentation |
| Qwen | qwen-turbo | dashscope.aliyuncs.com | Alibaba backed, good performance | Regional availability |

## Troubleshooting

### Common Issues

1. **"API key not found"**
   ```bash
   # Check current provider
   llmshell config get llm.provider
   
   # Set API key for current provider
   llmshell config api-key "your-key"
   ```

2. **"Provider not supported"**
   - Ensure you're using a supported provider: `openai`, `deepseek`, `doubao`, `qwen`
   - Check spelling and case sensitivity

3. **"Connection error"**
   - Verify your API key is correct
   - Check your internet connection
   - Ensure the provider's service is available in your region

4. **"Model not found"**
   - Check the model name is correct for your provider
   - Verify the model is available in your API plan

### Getting Help

```bash
# Show all configuration commands
llmshell config --help

# Show provider-specific help
llmshell config provider --help
llmshell config api-key --help
```

## Advanced Configuration

### Custom Base URLs
```bash
# Set custom base URL for a provider
llmshell config set llm.openai.base_url "https://your-custom-endpoint.com/v1"
```

### Provider-Specific Settings
```bash
# Set different temperatures for different providers
llmshell config set llm.openai.temperature 0.1
llmshell config set llm.deepseek.temperature 0.2
llmshell config set llm.doubao.temperature 0.15
llmshell config set llm.qwen.temperature 0.1
```

### Batch Configuration
```bash
# Configure all providers at once
for provider in openai deepseek doubao qwen; do
    llmshell config set "llm.$provider.temperature" 0.1
done
```

## Migration from Single Provider

If you were previously using only OpenAI:

1. **Your existing configuration will continue to work**
2. **To add other providers:**
   ```bash
   # Keep OpenAI as backup
   llmshell config api-key "your-openai-key" --provider openai
   
   # Add new provider
   llmshell config provider deepseek
   llmshell config api-key "your-deepseek-key"
   ```

3. **Switch between providers as needed:**
   ```bash
   llmshell config provider openai    # Use OpenAI
   llmshell config provider deepseek  # Use DeepSeek
   ```
