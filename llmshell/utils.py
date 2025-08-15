"""Utility functions for LLMShell."""

import os
import platform
import sys
from pathlib import Path
from typing import Optional

import shutil
from rich.console import Console

from llmshell.config import config

console = Console()


class CommandValidator:
    """Validates if commands exist in the system."""

    def __init__(self):
        """Initialize the command validator."""
        self.system = platform.system().lower()
        self._cache = {}

    def command_exists(self, command: str) -> bool:
        """Check if a command exists in the system PATH.

        Args:
            command: Command to check

        Returns:
            True if command exists, False otherwise
        """
        if command in self._cache:
            return self._cache[command]

        try:
            # Use shutil.which for cross-platform compatibility
            result = shutil.which(command)
            exists = result is not None
            self._cache[command] = exists
            return exists
        except Exception:
            self._cache[command] = False
            return False

    def get_command_path(self, command: str) -> Optional[str]:
        """Get the full path of a command.

        Args:
            command: Command to find

        Returns:
            Full path to command if found, None otherwise
        """
        try:
            return shutil.which(command)
        except Exception:
            return None

    def is_executable(self, command: str) -> bool:
        """Check if a command is executable.

        Args:
            command: Command to check

        Returns:
            True if executable, False otherwise
        """
        path = self.get_command_path(command)
        if not path:
            return False

        try:
            return os.access(path, os.X_OK)
        except Exception:
            return False


def setup_environment() -> None:
    """Setup the environment for LLMShell."""
    # Check for API key from config
    api_key = config.get_llm_api_key()
    provider = config.get_llm_provider()

    if not api_key:
        console.print(
            f"[yellow]Warning: {provider.title()} API key not found in configuration.[/yellow]"
        )
        console.print("Please set your API key:")
        console.print(
            f"  llmshell config api-key 'your-api-key-here' --provider {provider}"
        )
        console.print("  or edit the config file: llmshell config edit")

        # Fallback to environment variables for backward compatibility
        env_key = f"{provider.upper()}_API_KEY"
        env_api_key = os.getenv(env_key) or os.getenv("OPENAI_API_KEY")
        if env_api_key:
            console.print(
                f"[green]Using API key from environment variable {env_key}[/green]"
            )
            config.set_llm_api_key(env_api_key, provider)


def get_system_info() -> dict:
    """Get system information.

    Returns:
        Dictionary with system information
    """
    return {
        "platform": platform.system(),
        "platform_version": platform.version(),
        "architecture": platform.machine(),
        "python_version": sys.version,
        "python_executable": sys.executable,
    }


def sanitize_command(command: str) -> str:
    """Sanitize a command to prevent injection attacks.

    Args:
        command: Command to sanitize

    Returns:
        Sanitized command
    """
    # Check if sanitization is enabled
    if not config.get_enable_sanitization():
        return command

    # Basic sanitization - in a real application, you'd want more robust validation
    dangerous_patterns = [
        "rm -rf /",
        "rm -rf /*",
        "dd if=/dev/zero",
        "mkfs",
        "fdisk",
        "parted",
        "format",
    ]

    command_lower = command.lower()
    for pattern in dangerous_patterns:
        if pattern in command_lower:
            raise ValueError(f"Dangerous command pattern detected: {pattern}")

    return command


def format_command_output(output: str, max_lines: int = None) -> str:
    """Format command output for display.

    Args:
        output: Raw command output
        max_lines: Maximum number of lines to show (defaults to config)

    Returns:
        Formatted output
    """
    if max_lines is None:
        max_lines = config.get_max_output_lines()

    lines = output.split("\n")

    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines.append(f"... (truncated, showing first {max_lines} lines)")

    return "\n".join(lines)


def get_terminal_size() -> tuple:
    """Get terminal size.

    Returns:
        Tuple of (width, height)
    """
    try:
        import shutil

        return shutil.get_terminal_size()
    except Exception:
        return (80, 24)  # Default fallback


def is_interactive() -> bool:
    """Check if running in interactive mode.

    Returns:
        True if interactive, False otherwise
    """
    return sys.stdin.isatty() and sys.stdout.isatty()
