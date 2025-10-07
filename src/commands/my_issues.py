"""My Issues command for linear-cli."""

import json
import logging
from typing import Optional

import click

from src.client import LinearClient

logger = logging.getLogger(__name__)


@click.command(name="my-issues")
@click.option(
    "--limit", type=int, default=50, help="Maximum number of issues to return"
)
@click.option("--json", "json_output", is_flag=True, help="Output in JSON format")
@click.option("--token", help="Linear API token")
@click.pass_context
def my_issues(ctx, limit: int, json_output: bool, token: Optional[str]):
    """List issues assigned to you."""
    try:
        # Initialize client
        client = LinearClient(api_token=token)

        # Get current user's issues
        issues = client.get_my_issues(limit=limit)

        if not issues:
            if json_output:
                click.echo(json.dumps({"issues": [], "count": 0}, indent=2))
            else:
                click.echo("No issues assigned to you.")
            return

        # Output in JSON format
        if json_output:
            output_data = {"count": len(issues), "issues": issues}
            click.echo(json.dumps(output_data, indent=2))
            return

        # Display results in human-readable format
        click.echo(f"\nYou have {len(issues)} issue(s) assigned:\n")

        for issue in issues:
            click.echo(
                f"[{issue.get('identifier', 'N/A')}] {issue.get('title', 'N/A')}"
            )
            click.echo(
                f"  State: {issue.get('state', {}).get('name', 'N/A')} | Priority: {issue.get('priority', 'N/A')}"
            )
            click.echo(f"  URL: {issue.get('url', 'N/A')}")

            if issue.get("dueDate"):
                click.echo(f"  Due: {issue['dueDate']}")

            click.echo()

    except Exception as e:
        logger.error(f"Failed to get your issues: {e}")
        if json_output:
            click.echo(json.dumps({"error": str(e)}, indent=2), err=True)
        else:
            click.echo(f"Error: {e}", err=True)
        ctx.exit(1)
