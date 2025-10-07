"""Show command for linear-cli."""

import logging
from typing import Optional

import click

from src.client import LinearClient
from src.utils import format_issue

logger = logging.getLogger(__name__)


@click.command()
@click.argument("issue_id")
@click.option("--token", help="Linear API token")
@click.pass_context
def show(ctx, issue_id: str, token: Optional[str]):
    """Show details of a specific issue."""
    try:
        # Initialize client
        client = LinearClient(api_token=token)

        # Get issue
        issue = client.get_issue(issue_id)

        if not issue:
            click.echo(f"Issue not found: {issue_id}", err=True)
            ctx.exit(1)

        # Display result
        click.echo(format_issue(issue))

        # Display additional details
        if issue.get("assignee"):
            click.echo(
                f"\nAssignee: {issue['assignee'].get('name')} ({issue['assignee'].get('email')})"
            )

        if issue.get("creator"):
            click.echo(
                f"Creator: {issue['creator'].get('name')} ({issue['creator'].get('email')})"
            )

        click.echo(f"\nCreated: {issue.get('createdAt', 'N/A')}")
        click.echo(f"Updated: {issue.get('updatedAt', 'N/A')}")

    except Exception as e:
        logger.error(f"Failed to show issue: {e}")
        click.echo(f"Error: {e}", err=True)
        ctx.exit(1)
