"""Utility functions for logging and templates."""

import logging
import os
import sys
from typing import Optional


def setup_logging(log_file: Optional[str] = None, verbose: bool = False) -> None:
    """Set up logging configuration.

    Args:
        log_file: Path to log file. If None, logging to file is disabled.
        verbose: Enable verbose logging (DEBUG level).
    """
    log_level = logging.DEBUG if verbose else logging.INFO
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(console_handler)

    # File handler if log_file is specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(file_handler)


def get_template(template_name: Optional[str] = None) -> dict:
    """Get template configuration.

    Args:
        template_name: Name of the template to load.

    Returns:
        Dictionary containing template configuration.
    """
    # Check environment variable
    if not template_name:
        template_name = os.getenv("LINEAR_CLI_TEMPLATE")

    # Default template structure
    templates = {
        "default": {
            "title": "{title}",
            "description": "{description}",
            "priority": 2,
            "labels": [],
        },
        "bug": {
            "title": "[BUG] {title}",
            "description": "**Description:**\n{description}\n\n**Steps to Reproduce:**\n1. \n\n**Expected Behavior:**\n\n**Actual Behavior:**",
            "priority": 1,
            "labels": ["bug"],
        },
        "feature": {
            "title": "[FEATURE] {title}",
            "description": "**Feature Request:**\n{description}\n\n**Use Case:**\n\n**Proposed Solution:**",
            "priority": 3,
            "labels": ["feature"],
        },
    }

    return templates.get(template_name or "default", templates["default"])


def format_issue(issue: dict) -> str:
    """Format an issue for display.

    Args:
        issue: Issue dictionary from Linear API.

    Returns:
        Formatted string representation of the issue.
    """
    output = []
    output.append(f"ID: {issue.get('id', 'N/A')}")
    output.append(f"Title: {issue.get('title', 'N/A')}")
    output.append(f"State: {issue.get('state', {}).get('name', 'N/A')}")
    output.append(f"Priority: {issue.get('priority', 'N/A')}")
    output.append(f"URL: {issue.get('url', 'N/A')}")

    if issue.get("description"):
        output.append(f"Description: {issue['description']}")

    return "\n".join(output)


def get_config_value(
    key: str, default: Optional[str] = None, cli_value: Optional[str] = None
) -> Optional[str]:
    """Get configuration value from CLI argument or environment variable.

    Priority: CLI argument > Environment variable > Default

    Args:
        key: Configuration key (will be prefixed with LINEAR_CLI_).
        default: Default value if not found.
        cli_value: Value from CLI argument.

    Returns:
        Configuration value.
    """
    if cli_value:
        return cli_value

    env_key = f"LINEAR_CLI_{key.upper()}"
    return os.getenv(env_key, default)
