#!/bin/bash
# LLMShell - Natural language to system command translator
# Usage: ? <natural language command>

# Function to run LLMShell
run_llmshell() {
    # Check if Python and the package are available
    if command -v python3 &> /dev/null; then
        python3 -m llmshell.cli "$@"
    elif command -v python &> /dev/null; then
        python -m llmshell.cli "$@"
    else
        echo "Error: Python is not installed or not in PATH"
        return 1
    fi
}

# If no arguments provided, run interactive mode
if [ $# -eq 0 ]; then
    run_llmshell
else
    # Pass all arguments to the Python script
    run_llmshell "$@"
fi
