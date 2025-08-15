"""Core LLMShell functionality."""

import json
import subprocess
import sys
from typing import List, Optional, Tuple

import openai
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm
from rich.syntax import Syntax
from rich.table import Table
from shutil import which

from llmshell.config import config
from llmshell.llm import LLMTranslator
from llmshell.utils import CommandValidator

console = Console()


class LLMShell:
    """Main LLMShell class for processing natural language commands."""
    
    def __init__(
        self,
        model: str = None,
        temperature: float = None,
        provider: str = None,
        verbose: bool = False,
    ):
        """Initialize LLMShell.
        
        Args:
            model: LLM model to use for translation (defaults to config)
            temperature: Temperature for LLM generation (defaults to config)
            provider: LLM provider (defaults to config)
            verbose: Enable verbose output
        """
        self.provider = provider or config.get_llm_provider()
        self.model = model or config.get_llm_model(self.provider)
        self.temperature = temperature or config.get_llm_temperature(self.provider)
        self.verbose = verbose
        self.translator = LLMTranslator(model, temperature, provider)
        self.validator = CommandValidator()
        
    def process_command(self, user_input: str, force: bool = False) -> None:
        """Process a natural language command.
        
        Args:
            user_input: Natural language command from user
            force: Execute without confirmation
        """
        console.print(f"\n[bold cyan]Processing:[/bold cyan] {user_input}")
        
        try:
            # Step 1: Translate to system commands
            commands = self.translator.translate(user_input)
            
            if not commands:
                console.print("[red]No commands generated. Please try a different input.[/red]")
                return
                
            # Step 2: Validate commands
            valid_commands = self._validate_commands(commands)
            
            if not valid_commands:
                console.print("[red]No valid commands found. Please try a different input.[/red]")
                return
                
            # Step 3: Display commands
            self._display_commands(valid_commands, user_input)
            
            # Step 4: Execute if confirmed
            if force or (config.get_show_confirmations() and self._confirm_execution(valid_commands)):
                self._execute_commands(valid_commands)
                
        except Exception as e:
            console.print(f"[red]Error processing command: {e}[/red]")
            if self.verbose:
                console.print_exception()
    
    def interactive_mode(self) -> None:
        """Run interactive mode with continuous command processing."""
        console.print("[bold blue]Interactive Mode[/bold blue]")
        console.print("Type natural language commands. Type 'exit' to quit.\n")
        
        while True:
            try:
                user_input = input("? ")
                
                if user_input.lower() in ["exit", "quit"]:
                    break
                    
                if user_input.strip():
                    self.process_command(user_input)
                    
            except KeyboardInterrupt:
                console.print("\n[yellow]Use 'exit' to quit[/yellow]")
            except EOFError:
                break
                
        console.print("[yellow]Goodbye![/yellow]")
    
    def _validate_commands(self, commands: List[str]) -> List[Tuple[str, bool]]:
        """Validate which commands exist in the system.
        
        Args:
            commands: List of commands to validate
            
        Returns:
            List of tuples (command, exists)
        """
        valid_commands = []
        
        for cmd in commands:
            # Extract the base command (first word)
            base_cmd = cmd.split()[0] if cmd.strip() else ""
            
            if base_cmd:
                exists = self.validator.command_exists(base_cmd)
                valid_commands.append((cmd, exists))
                
                if self.verbose:
                    status = "[green]✓[/green]" if exists else "[red]✗[/red]"
                    console.print(f"  {status} {cmd}")
        
        return valid_commands
    
    def _display_commands(self, valid_commands: List[Tuple[str, bool]], original_input: str) -> None:
        """Display the translated commands in a nice format.
        
        Args:
            valid_commands: List of (command, exists) tuples
            original_input: Original user input
        """
        table = Table(title=f"Commands for: {original_input}")
        table.add_column("Command", style="cyan", no_wrap=True)
        table.add_column("Status", style="green")
        table.add_column("Description", style="white")
        
        for cmd, exists in valid_commands:
            status = "Available" if exists else "Not Found"
            status_style = "green" if exists else "red"
            
            # Try to get a brief description
            description = self._get_command_description(cmd)
            
            table.add_row(
                cmd,
                f"[{status_style}]{status}[/{status_style}]",
                description
            )
        
        console.print(table)
    
    def _get_command_description(self, command: str) -> str:
        """Get a brief description of what a command does.
        
        Args:
            command: The command to describe
            
        Returns:
            Brief description of the command
        """
        base_cmd = command.split()[0]
        
        descriptions = {
            "ls": "List directory contents",
            "cat": "Display file contents",
            "grep": "Search for patterns in files",
            "find": "Find files and directories",
            "ps": "Show process status",
            "top": "Display system processes",
            "df": "Show disk space usage",
            "du": "Show directory space usage",
            "netstat": "Show network statistics",
            "ifconfig": "Configure network interfaces",
            "ip": "Show/manipulate routing",
            "ping": "Test network connectivity",
            "curl": "Transfer data from/to servers",
            "wget": "Retrieve files from web",
            "tar": "Archive files",
            "zip": "Compress files",
            "unzip": "Extract compressed files",
            "chmod": "Change file permissions",
            "chown": "Change file ownership",
            "sudo": "Execute command as superuser",
        }
        
        return descriptions.get(base_cmd, "System command")
    
    def _confirm_execution(self, valid_commands: List[Tuple[str, bool]]) -> bool:
        """Ask user to confirm command execution.
        
        Args:
            valid_commands: List of (command, exists) tuples
            
        Returns:
            True if user confirms, False otherwise
        """
        available_commands = [cmd for cmd, exists in valid_commands if exists]
        
        if not available_commands:
            console.print("[yellow]No available commands to execute.[/yellow]")
            return False
            
        if len(available_commands) == 1:
            return Confirm.ask(f"Execute: [cyan]{available_commands[0]}[/cyan]?")
        else:
            console.print("\n[bold]Available commands:[/bold]")
            for i, cmd in enumerate(available_commands, 1):
                console.print(f"  {i}. [cyan]{cmd}[/cyan]")
            
            try:
                choice = int(input("\nSelect command to execute (number): ")) - 1
                if 0 <= choice < len(available_commands):
                    return Confirm.ask(f"Execute: [cyan]{available_commands[choice]}[/cyan]?")
                else:
                    console.print("[red]Invalid selection.[/red]")
                    return False
            except (ValueError, IndexError):
                console.print("[red]Invalid input.[/red]")
                return False
    
    def _execute_commands(self, valid_commands: List[Tuple[str, bool]]) -> None:
        """Execute the selected commands.
        
        Args:
            valid_commands: List of (command, exists) tuples
        """
        available_commands = [cmd for cmd, exists in valid_commands if exists]
        
        if not available_commands:
            return
            
        # For now, execute the first available command
        # In the future, this could be enhanced to execute multiple commands
        command = available_commands[0]
        
        console.print(f"\n[bold green]Executing:[/bold green] {command}")
        console.print("-" * 50)
        
        try:
            # Execute the command
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=config.get_timeout_seconds()
            )
            
            # Display output
            if result.stdout:
                console.print("[bold]Output:[/bold]")
                console.print(Syntax(result.stdout, "bash", theme=config.get_theme()))
                
            if result.stderr:
                console.print("[bold red]Errors:[/bold red]")
                console.print(Syntax(result.stderr, "bash", theme=config.get_theme()))
                
            if result.returncode != 0:
                console.print(f"[red]Command exited with code: {result.returncode}[/red]")
            else:
                console.print("[green]Command executed successfully![/green]")
                
        except subprocess.TimeoutExpired:
            console.print(f"[red]Command timed out after {config.get_timeout_seconds()} seconds.[/red]")
        except Exception as e:
            console.print(f"[red]Error executing command: {e}[/red]")
