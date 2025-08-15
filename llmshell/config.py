"""Configuration management for LLMShell."""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

from rich.console import Console

console = Console()

DEFAULT_CONFIG = {
    "llm": {
        "provider": "openai",  # openai, deepseek, doubao, qwen
        "openai": {
            "api_key": "",
            "model": "gpt-3.5-turbo",
            "temperature": 0.1,
            "base_url": "https://api.openai.com/v1",
        },
        "deepseek": {
            "api_key": "",
            "model": "deepseek-chat",
            "temperature": 0.1,
            "base_url": "https://api.deepseek.com/v1",
        },
        "doubao": {
            "api_key": "",
            "model": "doubao-pro",
            "temperature": 0.1,
            "base_url": "https://api.doubao.com/v1",
        },
        "qwen": {
            "api_key": "",
            "model": "qwen-turbo",
            "temperature": 0.1,
            "base_url": "https://dashscope.aliyuncs.com/api/v1",
        },
    },
    "ui": {
        "theme": "monokai",
        "max_output_lines": 50,
        "show_confirmations": True,
    },
    "safety": {
        "enable_sanitization": True,
        "timeout_seconds": 30,
    },
}

CONFIG_FILE = Path.home() / ".llmshell.config"


class ConfigManager:
    """Manages LLMShell configuration."""
    
    def __init__(self, config_file: Optional[Path] = None):
        """Initialize configuration manager.
        
        Args:
            config_file: Path to configuration file (defaults to ~/.llmshell.config)
        """
        self.config_file = config_file or CONFIG_FILE
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file.
        
        Returns:
            Configuration dictionary
        """
        if not self.config_file.exists():
            # Create default config
            self._save_config(DEFAULT_CONFIG)
            return DEFAULT_CONFIG.copy()
        
        try:
            with open(self.config_file, "r") as f:
                config = json.load(f)
            
            # Merge with defaults to ensure all keys exist
            merged_config = self._merge_with_defaults(config)
            return merged_config
            
        except (json.JSONDecodeError, IOError) as e:
            console.print(f"[yellow]Warning: Could not load config from {self.config_file}: {e}[/yellow]")
            console.print("[yellow]Using default configuration.[/yellow]")
            return DEFAULT_CONFIG.copy()
    
    def _save_config(self, config: Dict[str, Any]) -> None:
        """Save configuration to file.
        
        Args:
            config: Configuration dictionary to save
        """
        try:
            # Ensure directory exists
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_file, "w") as f:
                json.dump(config, f, indent=2)
                
        except IOError as e:
            console.print(f"[red]Error saving config to {self.config_file}: {e}[/red]")
    
    def _merge_with_defaults(self, user_config: Dict[str, Any]) -> Dict[str, Any]:
        """Merge user config with defaults.
        
        Args:
            user_config: User configuration
            
        Returns:
            Merged configuration
        """
        merged = DEFAULT_CONFIG.copy()
        
        def merge_dicts(default: Dict[str, Any], user: Dict[str, Any]) -> None:
            for key, value in user.items():
                if key in default and isinstance(default[key], dict) and isinstance(value, dict):
                    merge_dicts(default[key], value)
                else:
                    default[key] = value
        
        merge_dicts(merged, user_config)
        return merged
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value.
        
        Args:
            key: Configuration key (supports dot notation like 'llm.openai.model')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split(".")
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value.
        
        Args:
            key: Configuration key (supports dot notation like 'llm.openai.model')
            value: Value to set
        """
        keys = key.split(".")
        config = self.config
        
        # Navigate to the parent of the target key
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Set the value
        config[keys[-1]] = value
        
        # Save the updated config
        self._save_config(self.config)
    
    # LLM Provider Management
    def get_llm_provider(self) -> str:
        """Get the current LLM provider.
        
        Returns:
            Provider name
        """
        return self.get("llm.provider", "openai")
    
    def set_llm_provider(self, provider: str) -> None:
        """Set the LLM provider.
        
        Args:
            provider: Provider name (openai, deepseek, doubao, qwen)
        """
        self.set("llm.provider", provider)
    
    def get_llm_api_key(self) -> Optional[str]:
        """Get API key for the current LLM provider.
        
        Returns:
            API key if found, None otherwise
        """
        provider = self.get_llm_provider()
        api_key = self.get(f"llm.{provider}.api_key")
        if api_key:
            return api_key
        
        # Fallback to environment variable for backward compatibility
        env_key = f"{provider.upper()}_API_KEY"
        return os.getenv(env_key) or os.getenv("OPENAI_API_KEY")
    
    def set_llm_api_key(self, api_key: str, provider: str = None) -> None:
        """Set API key for an LLM provider.
        
        Args:
            api_key: API key
            provider: Provider name (defaults to current provider)
        """
        if provider is None:
            provider = self.get_llm_provider()
        self.set(f"llm.{provider}.api_key", api_key)
    
    def get_llm_model(self, provider: str = None) -> str:
        """Get the LLM model for a provider.
        
        Args:
            provider: Provider name (defaults to current provider)
            
        Returns:
            Model name
        """
        if provider is None:
            provider = self.get_llm_provider()
        return self.get(f"llm.{provider}.model", "gpt-3.5-turbo")
    
    def get_llm_temperature(self, provider: str = None) -> float:
        """Get the temperature for a provider.
        
        Args:
            provider: Provider name (defaults to current provider)
            
        Returns:
            Temperature value
        """
        if provider is None:
            provider = self.get_llm_provider()
        return self.get(f"llm.{provider}.temperature", 0.1)
    
    def get_llm_base_url(self, provider: str = None) -> str:
        """Get the base URL for a provider.
        
        Args:
            provider: Provider name (defaults to current provider)
            
        Returns:
            Base URL
        """
        if provider is None:
            provider = self.get_llm_provider()
        return self.get(f"llm.{provider}.base_url", "")
    
    # Backward compatibility methods
    def get_openai_api_key(self) -> Optional[str]:
        """Get OpenAI API key (backward compatibility).
        
        Returns:
            API key if found, None otherwise
        """
        return self.get_llm_api_key() if self.get_llm_provider() == "openai" else None
    
    def set_openai_api_key(self, api_key: str) -> None:
        """Set OpenAI API key (backward compatibility).
        
        Args:
            api_key: OpenAI API key
        """
        self.set_llm_api_key(api_key, "openai")
    
    def get_model(self) -> str:
        """Get the LLM model (backward compatibility).
        
        Returns:
            Model name
        """
        return self.get_llm_model()
    
    def get_temperature(self) -> float:
        """Get the temperature (backward compatibility).
        
        Returns:
            Temperature value
        """
        return self.get_llm_temperature()
    
    # UI and Safety settings
    def get_theme(self) -> str:
        """Get the UI theme.
        
        Returns:
            Theme name
        """
        return self.get("ui.theme", "monokai")
    
    def get_max_output_lines(self) -> int:
        """Get maximum output lines.
        
        Returns:
            Maximum number of lines
        """
        return self.get("ui.max_output_lines", 50)
    
    def get_show_confirmations(self) -> bool:
        """Get whether to show confirmations.
        
        Returns:
            True if confirmations should be shown
        """
        return self.get("ui.show_confirmations", True)
    
    def get_timeout_seconds(self) -> int:
        """Get command timeout in seconds.
        
        Returns:
            Timeout in seconds
        """
        return self.get("safety.timeout_seconds", 30)
    
    def get_enable_sanitization(self) -> bool:
        """Get whether command sanitization is enabled.
        
        Returns:
            True if sanitization is enabled
        """
        return self.get("safety.enable_sanitization", True)
    
    def show_config(self) -> None:
        """Display current configuration."""
        console.print(f"[bold]Configuration file:[/bold] {self.config_file}")
        console.print(f"[bold]Current LLM provider:[/bold] {self.get_llm_provider()}")
        console.print()
        
        # Hide API keys for security
        safe_config = self.config.copy()
        for provider in ["openai", "deepseek", "doubao", "qwen"]:
            if "llm" in safe_config and provider in safe_config["llm"]:
                api_key = safe_config["llm"][provider].get("api_key", "")
                if api_key:
                    safe_config["llm"][provider]["api_key"] = "*" * min(len(api_key), 8) + "..."
                else:
                    safe_config["llm"][provider]["api_key"] = "(not set)"
        
        console.print_json(data=safe_config)
    
    def edit_config(self) -> None:
        """Open configuration file for editing."""
        try:
            # Ensure config file exists
            if not self.config_file.exists():
                self._save_config(DEFAULT_CONFIG)
            
            # Try to open with default editor
            editor = os.getenv("EDITOR", "nano")
            os.system(f"{editor} {self.config_file}")
            
            # Reload config after editing
            self.config = self._load_config()
            console.print("[green]Configuration reloaded.[/green]")
            
        except Exception as e:
            console.print(f"[red]Error editing config: {e}[/red]")
            console.print(f"Please edit {self.config_file} manually.")


# Global config instance
config = ConfigManager()
