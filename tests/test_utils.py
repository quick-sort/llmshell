"""Tests for utility functions."""

import pytest
from llmshell.utils import CommandValidator, sanitize_command, format_command_output


class TestCommandValidator:
    """Test CommandValidator class."""
    
    def test_command_exists(self):
        """Test command existence checking."""
        validator = CommandValidator()
        
        # Test with common commands that should exist
        assert validator.command_exists("ls") or validator.command_exists("dir")
        assert validator.command_exists("echo")
        
        # Test with non-existent command
        assert not validator.command_exists("nonexistentcommand12345")
    
    def test_get_command_path(self):
        """Test getting command path."""
        validator = CommandValidator()
        
        # Test with existing command
        path = validator.get_command_path("ls")
        if path:
            assert isinstance(path, str)
            assert len(path) > 0
        
        # Test with non-existent command
        assert validator.get_command_path("nonexistentcommand12345") is None


class TestSanitizeCommand:
    """Test command sanitization."""
    
    def test_safe_commands(self):
        """Test that safe commands pass sanitization."""
        safe_commands = [
            "ls -la",
            "echo hello",
            "cat file.txt",
            "grep pattern file.txt"
        ]
        
        for cmd in safe_commands:
            assert sanitize_command(cmd) == cmd
    
    def test_dangerous_commands(self):
        """Test that dangerous commands are caught."""
        dangerous_commands = [
            "rm -rf /",
            "rm -rf /*",
            "dd if=/dev/zero",
            "mkfs.ext4 /dev/sda1"
        ]
        
        for cmd in dangerous_commands:
            with pytest.raises(ValueError):
                sanitize_command(cmd)


class TestFormatCommandOutput:
    """Test command output formatting."""
    
    def test_short_output(self):
        """Test formatting of short output."""
        output = "line1\nline2\nline3"
        formatted = format_command_output(output, max_lines=5)
        assert formatted == output
    
    def test_long_output_truncation(self):
        """Test truncation of long output."""
        output = "\n".join([f"line{i}" for i in range(100)])
        formatted = format_command_output(output, max_lines=10)
        
        lines = formatted.split('\n')
        assert len(lines) == 11  # 10 lines + truncation message
        assert "truncated" in lines[-1]
    
    def test_empty_output(self):
        """Test formatting of empty output."""
        formatted = format_command_output("", max_lines=10)
        assert formatted == ""
