"""Main CLI entry point for linear-cli."""

import os
import sys

import click

from src.commands.create import create
from src.commands.list import list
from src.commands.my_issues import my_issues
from src.commands.search import search
from src.commands.show import show
from src.utils import get_config_value, setup_logging


@click.group()
@click.option("--log", is_flag=True, help="Enable logging to file")
@click.option(
    "--log-file",
    default="linear-cli.log",
    help="Log file path (default: linear-cli.log)",
)
@click.option("--verbose", is_flag=True, help="Enable verbose output")
@click.option(
    "--template", help="Template name to use (can also be set via LINEAR_CLI_TEMPLATE)"
)
@click.pass_context
def cli(ctx, log: bool, log_file: str, verbose: bool, template: str):
    """Linear CLI - A command-line interface for Linear.

    Environment Variables:
        LINEAR_CLI_TOKEN    - Linear API token (required)
        LINEAR_CLI_TEAM_ID  - Default team ID
        LINEAR_CLI_TEMPLATE - Default template name
    """
    # Ensure context object exists
    ctx.ensure_object(dict)

    # Setup logging
    if log:
        # Check for custom log file in environment
        log_file = get_config_value("LOG_FILE", log_file, log_file)
        setup_logging(log_file=log_file, verbose=verbose)
    else:
        setup_logging(log_file=None, verbose=verbose)

    # Store global options in context
    ctx.obj["verbose"] = verbose
    ctx.obj["template"] = template or os.getenv("LINEAR_CLI_TEMPLATE")


# Register commands
cli.add_command(create)
cli.add_command(show)
cli.add_command(list)
cli.add_command(search)
cli.add_command(my_issues)


def main():
    """Main entry point."""
    try:
        cli(obj={})
    except KeyboardInterrupt:
        click.echo("\n\nInterrupted by user", err=True)
        sys.exit(130)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
