"""LLM translation module for converting natural language to system commands."""

import json
import os
from typing import List, Optional

import openai
from rich.console import Console

from llmshell.config import config

console = Console()


class LLMTranslator:
    """Translates natural language to system commands using LLM."""

    def __init__(
        self, model: str = None, temperature: float = None, provider: str = None
    ):
        """Initialize the LLM translator.

        Args:
            model: LLM model to use (defaults to config)
            temperature: Temperature for generation (defaults to config)
            provider: LLM provider (defaults to config)
        """
        self.provider = provider or config.get_llm_provider()
        self.model = model or config.get_llm_model(self.provider)
        self.temperature = temperature or config.get_llm_temperature(self.provider)
        self.base_url = config.get_llm_base_url(self.provider)

        api_key = config.get_llm_api_key()
        if not api_key:
            self.client = None
        else:
            self.client = self._create_client(api_key)

        # System prompt for command translation
        self.system_prompt = """You are a command-line assistant that translates natural language requests into system commands.

Your task is to:
1. Understand the user's intent
2. Generate appropriate system commands (bash/shell commands)
3. Return ONLY valid, executable commands
4. Prefer common, widely-available commands
5. Include necessary flags and arguments
6. Return multiple options when appropriate

Rules:
- Return only the command(s), no explanations
- Use standard Unix/Linux commands when possible
- Include file paths and arguments as needed
- For network operations, use common tools like curl, wget, ping, etc.
- For file operations, use ls, find, grep, cat, etc.
- For system info, use ps, top, df, du, etc.
- Return up to 3 different command options if applicable

Format your response as a JSON array of strings, each containing a single command.

Examples:
Input: "show network ip"
Output: ["ip addr show", "ifconfig", "hostname -I"]

Input: "find large files"
Output: ["find . -type f -size +100M", "du -h | sort -hr | head -10"]

Input: "check system memory"
Output: ["free -h", "top -l 1 | head -10", "vm_stat"]"""

    def _create_client(self, api_key: str):
        """Create the appropriate client for the current provider.

        Args:
            api_key: API key for the provider

        Returns:
            Client instance
        """
        if self.provider == "openai":
            return openai.OpenAI(
                api_key=api_key, base_url=self.base_url if self.base_url else None
            )
        elif self.provider == "deepseek":
            return openai.OpenAI(api_key=api_key, base_url=self.base_url)
        elif self.provider == "doubao":
            return openai.OpenAI(api_key=api_key, base_url=self.base_url)
        elif self.provider == "qwen":
            return openai.OpenAI(api_key=api_key, base_url=self.base_url)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def translate(self, user_input: str) -> List[str]:
        """Translate natural language to system commands.

        Args:
            user_input: Natural language command from user

        Returns:
            List of system commands
        """
        if not self.client:
            # No API key available, use fallback
            return self._fallback_translation(user_input)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_input},
                ],
                temperature=self.temperature,
                max_tokens=500,
            )

            content = response.choices[0].message.content.strip()

            # Try to parse as JSON first
            try:
                commands = json.loads(content)
                if isinstance(commands, list):
                    return [cmd.strip() for cmd in commands if cmd.strip()]
            except json.JSONDecodeError:
                pass

            # Fallback: split by newlines and clean up
            commands = []
            for line in content.split("\n"):
                line = line.strip()
                if line and not line.startswith("#") and not line.startswith("//"):
                    # Remove any markdown formatting
                    if line.startswith("`") and line.endswith("`"):
                        line = line[1:-1]
                    commands.append(line)

            return commands

        except Exception as e:
            console.print(
                f"[red]Error translating command with {self.provider}: {e}[/red]"
            )
            # Fallback to predefined mappings
            return self._fallback_translation(user_input)

    def translate_with_fallback(self, user_input: str) -> List[str]:
        """Translate with fallback to common command mappings.

        Args:
            user_input: Natural language command from user

        Returns:
            List of system commands
        """
        # Try LLM translation first
        commands = self.translate(user_input)

        if commands:
            return commands

        # Fallback to common mappings
        return self._fallback_translation(user_input)

    def _fallback_translation(self, user_input: str) -> List[str]:
        """Fallback translation using common command mappings.

        Args:
            user_input: Natural language command from user

        Returns:
            List of system commands
        """
        input_lower = user_input.lower()

        # Common command mappings
        mappings = {
            "show network ip": ["ip addr show", "ifconfig", "hostname -I"],
            "show ip": ["ip addr show", "ifconfig", "hostname -I"],
            "network ip": ["ip addr show", "ifconfig", "hostname -I"],
            "check memory": ["free -h", "top -l 1 | head -10", "vm_stat"],
            "system memory": ["free -h", "top -l 1 | head -10", "vm_stat"],
            "memory usage": ["free -h", "top -l 1 | head -10", "vm_stat"],
            "disk space": ["df -h", "du -h | sort -hr | head -10"],
            "disk usage": ["df -h", "du -h | sort -hr | head -10"],
            "list files": ["ls -la", "ls -lh"],
            "show files": ["ls -la", "ls -lh"],
            "running processes": ["ps aux", "top", "htop"],
            "process list": ["ps aux", "top", "htop"],
            "system processes": ["ps aux", "top", "htop"],
            "find large files": [
                "find . -type f -size +100M",
                "du -h | sort -hr | head -10",
            ],
            "search files": ["find . -name '*pattern*'", "grep -r 'pattern' ."],
            "ping google": ["ping -c 4 google.com", "ping google.com"],
            "test connection": ["ping -c 4 google.com", "curl -I https://google.com"],
            "current directory": ["pwd", "ls -la"],
            "working directory": ["pwd", "ls -la"],
            "system info": ["uname -a", "cat /etc/os-release", "systeminfo"],
            "os info": ["uname -a", "cat /etc/os-release", "systeminfo"],
            "cpu info": [
                "lscpu",
                "cat /proc/cpuinfo",
                "sysctl -n machdep.cpu.brand_string",
            ],
            "uptime": ["uptime", "w"],
            "who is logged in": ["who", "w", "users"],
            "logged users": ["who", "w", "users"],
        }

        # Check for exact matches first
        for pattern, commands in mappings.items():
            if pattern in input_lower:
                return commands

        # Check for partial matches
        for pattern, commands in mappings.items():
            if any(word in input_lower for word in pattern.split()):
                return commands

        return []
