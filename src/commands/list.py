"""List command for linear-cli."""

import logging
from typing import Optional

import click

from src.client import LinearClient

logger = logging.getLogger(__name__)


@click.command()
@click.option("--team-id", help="Filter by team ID")
@click.option(
    "--limit", type=int, default=50, help="Maximum number of issues to return"
)
@click.option("--token", help="Linear API token")
@click.pass_context
def list(ctx, team_id: Optional[str], limit: int, token: Optional[str]):
    """List issues from Linear."""
    try:
        # Get team ID from environment if not provided
        if not team_id:
            from src.utils import get_config_value

            team_id = get_config_value("TEAM_ID")

        # Initialize client
        client = LinearClient(api_token=token)

        # List issues
        issues = client.list_issues(team_id=team_id, limit=limit)

        if not issues:
            click.echo("No issues found.")
            return

        # Display results
        click.echo(f"\nFound {len(issues)} issue(s):\n")

        for issue in issues:
            click.echo(
                f"[{issue.get('identifier', 'N/A')}] {issue.get('title', 'N/A')}"
            )
            click.echo(
                f"  State: {issue.get('state', {}).get('name', 'N/A')} | Priority: {issue.get('priority', 'N/A')}"
            )
            click.echo(f"  URL: {issue.get('url', 'N/A')}")
            click.echo()

    except Exception as e:
        logger.error(f"Failed to list issues: {e}")
        click.echo(f"Error: {e}", err=True)
        ctx.exit(1)
