#!/usr/bin/env python3
"""Demo script for LLMShell functionality."""

import os
from llmshell.core import LLMShell
from llmshell.utils import setup_environment


def main():
    """Run a demo of LLMShell functionality."""
    print("LLMShell Demo")
    print("=" * 50)

    # Setup environment
    setup_environment()

    # Initialize LLMShell (will use fallback if no API key)
    try:
        shell = LLMShell(verbose=True)
    except Exception as e:
        print(f"Warning: Could not initialize LLMShell with API: {e}")
        print("Using fallback translation only...")
        return

    # Demo commands
    demo_commands = [
        "show network ip",
        "check system memory",
        "list files in current directory",
        "find large files",
        "show running processes",
    ]

    print("\nDemo commands that will be processed:")
    for i, cmd in enumerate(demo_commands, 1):
        print(f"{i}. {cmd}")

    print("\nNote: This is a demo. Commands will be translated but not executed.")
    print("To actually run commands, use the interactive mode or CLI.")

    # Process each command
    for cmd in demo_commands:
        print(f"\n{'=' * 50}")
        print(f"Processing: {cmd}")
        print("=" * 50)

        try:
            # Translate the command
            commands = shell.translator.translate(cmd)
            print(f"Translated commands: {commands}")

            # Validate commands
            valid_commands = shell._validate_commands(commands)
            print(f"Valid commands: {valid_commands}")

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
