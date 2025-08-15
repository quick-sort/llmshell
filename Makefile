.PHONY: install setup test clean lint format help

# Default target
help:
	@echo "LLMShell - Natural language to system command translator"
	@echo ""
	@echo "Available targets:"
	@echo "  install    - Install dependencies using uv"
	@echo "  setup      - Setup the project (install + create symlink)"
	@echo "  test       - Run tests"
	@echo "  lint       - Run linting"
	@echo "  format     - Format code"
	@echo "  clean      - Clean up generated files"
	@echo "  run        - Run the interactive shell"
	@echo "  help       - Show this help message"

# Install dependencies
install:
	@echo "Installing dependencies with uv..."
	uv sync
	@echo "Dependencies installed successfully!"

# Setup the project
setup: install
	@echo "Setting up LLMShell..."
	@echo "Configuration will be stored in ~/.llmshell.config"
	@echo "Setup complete! Don't forget to:"
	@echo "1. Set your OpenAI API key: llmshell config set openai.api_key 'your-key'"
	@echo "2. Run 'make run' to start using LLMShell"

# Run tests
test:
	@echo "Running tests..."
	uv run pytest tests/ -v

# Run linting
lint:
	@echo "Running linting..."
	uv run flake8 llmshell/ tests/
	uv run black --check llmshell/ tests/
	uv run isort --check-only llmshell/ tests/

# Format code
format:
	@echo "Formatting code..."
	uv run black llmshell/ tests/
	uv run isort llmshell/ tests/

# Clean up
clean:
	@echo "Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf build/
	rm -rf dist/

# Run the interactive shell
run:
	@echo "Starting LLMShell..."
	uv run python run.py

# Install the package in development mode
dev-install:
	@echo "Installing in development mode..."
	uv pip install -e .

# Create a symlink for the '?' command (requires sudo)
install-symlink:
	@echo "Creating symlink for '?' command..."
	@if [ -w /usr/local/bin ]; then \
		ln -sf $(PWD)/llmshell.sh /usr/local/bin/?; \
		echo "Symlink created! You can now use '?' command from anywhere"; \
	else \
		echo "Cannot write to /usr/local/bin. Try running with sudo:"; \
		echo "sudo make install-symlink"; \
	fi
