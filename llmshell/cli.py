"""Main CLI module for LLMShell."""

import os
import sys
from typing import Optional

import typer
from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.syntax import Syntax

from llmshell.config import config
from llmshell.core import LLMShell
from llmshell.utils import setup_environment

app = typer.Typer(
    name="llmshell",
    help="Natural language to system command translator",
    add_completion=False,
)

# Create subcommands for configuration
config_app = typer.Typer(help="Configuration management")
app.add_typer(config_app, name="config")

console = Console()


@app.command()
def main(
    command: Optional[str] = typer.Argument(
        None,
        help="Natural language command to translate and execute",
    ),
    model: str = typer.Option(
        None,
        "--model",
        "-m",
        help="LLM model to use for translation (defaults to config)",
    ),
    temperature: float = typer.Option(
        None,
        "--temperature",
        "-t",
        help="Temperature for LLM generation (0.0-1.0, defaults to config)",
        min=0.0,
        max=1.0,
    ),
    provider: str = typer.Option(
        None,
        "--provider",
        "-p",
        help="LLM provider (openai, deepseek, doubao, qwen, defaults to config)",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Execute command without confirmation",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable verbose output",
    ),
) -> None:
    """LLMShell - Translate natural language to system commands."""
    try:
        # Setup environment
        setup_environment()

        # Initialize LLMShell
        shell = LLMShell(model=model, temperature=temperature, provider=provider, verbose=verbose)

        if command:
            # Single command mode
            shell.process_command(command, force=force)
        else:
            # Interactive mode
            shell.interactive_mode()

    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        if verbose:
            console.print_exception()
        sys.exit(1)


@config_app.command("show")
def show_config() -> None:
    """Show current configuration."""
    config.show_config()


@config_app.command("edit")
def edit_config() -> None:
    """Edit configuration file."""
    config.edit_config()


@config_app.command("set")
def set_config(
    key: str = typer.Argument(..., help="Configuration key (e.g., 'openai.model')"),
    value: str = typer.Argument(..., help="Value to set"),
) -> None:
    """Set a configuration value."""
    config.set(key, value)
    console.print(f"[green]Set {key} = {value}[/green]")


@config_app.command("get")
def get_config(
    key: str = typer.Argument(..., help="Configuration key (e.g., 'llm.openai.model')"),
) -> None:
    """Get a configuration value."""
    value = config.get(key)
    console.print(f"{key} = {value}")


@config_app.command("provider")
def set_provider(
    provider: str = typer.Argument(..., help="LLM provider (openai, deepseek, doubao, qwen)"),
) -> None:
    """Set the LLM provider."""
    if provider not in ["openai", "deepseek", "doubao", "qwen"]:
        console.print("[red]Invalid provider. Must be one of: openai, deepseek, doubao, qwen[/red]")
        return
    
    config.set_llm_provider(provider)
    console.print(f"[green]Set LLM provider to: {provider}[/green]")


@config_app.command("api-key")
def set_api_key(
    api_key: str = typer.Argument(..., help="API key for the current provider"),
    provider: str = typer.Option(None, "--provider", "-p", help="Provider name (defaults to current)"),
) -> None:
    """Set API key for an LLM provider."""
    if provider and provider not in ["openai", "deepseek", "doubao", "qwen"]:
        console.print("[red]Invalid provider. Must be one of: openai, deepseek, doubao, qwen[/red]")
        return
    
    config.set_llm_api_key(api_key, provider)
    target_provider = provider or config.get_llm_provider()
    console.print(f"[green]Set API key for {target_provider}[/green]")


@config_app.command("list-providers")
def list_providers() -> None:
    """List available LLM providers and their status."""
    current_provider = config.get_llm_provider()
    
    console.print(f"[bold]Current provider:[/bold] {current_provider}")
    console.print()
    
    providers = ["openai", "deepseek", "doubao", "qwen"]
    for provider in providers:
        api_key = config.get(f"llm.{provider}.api_key")
        model = config.get(f"llm.{provider}.model")
        status = "[green]✓[/green] Configured" if api_key else "[red]✗[/red] Not configured"
        
        console.print(f"[bold]{provider.title()}:[/bold] {status}")
        console.print(f"  Model: {model}")
        if api_key:
            console.print(f"  API Key: {'*' * min(len(api_key), 8)}...")
        console.print()


def run_interactive() -> None:
    """Run the interactive shell with '?' prompt."""
    console.print(
        "[bold blue]LLMShell[/bold blue] - Natural language to system commands"
    )
    console.print("Type 'exit' or 'quit' to exit, 'help' for help\n")

    try:
        setup_environment()
        shell = LLMShell()

        while True:
            try:
                # Get user input with '?' prompt
                user_input = Prompt.ask("?")

                if user_input.lower() in ["exit", "quit"]:
                    console.print("[yellow]Goodbye![/yellow]")
                    break
                elif user_input.lower() in ["help", "?"]:
                    show_help()
                    continue
                elif not user_input.strip():
                    continue

                shell.process_command(user_input)

            except KeyboardInterrupt:
                console.print("\n[yellow]Use 'exit' or 'quit' to exit[/yellow]")
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")

    except Exception as e:
        console.print(f"[red]Failed to start interactive mode: {e}[/red]")
        sys.exit(1)


def show_help() -> None:
    """Show help information."""
    help_text = """
[bold]LLMShell Commands:[/bold]

• [green]exit[/green] or [green]quit[/green] - Exit the shell
• [green]help[/green] or [green]?[/green] - Show this help

[bold]Examples:[/bold]
• [cyan]show network ip[/cyan] - Get network IP information
• [cyan]find large files[/cyan] - Find large files in current directory
• [cyan]check system memory[/cyan] - Check system memory usage
• [cyan]list running processes[/cyan] - List running processes

[bold]Tips:[/bold]
• Be specific in your requests for better command translation
• The system will show you the command before executing it
• You can always cancel execution if the command doesn't look right
"""
    console.print(help_text)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # No arguments provided, run interactive mode
        run_interactive()
    else:
        # Arguments provided, run command mode
        app()
