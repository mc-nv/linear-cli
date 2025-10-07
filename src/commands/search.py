"""Search command for linear-cli."""

import logging
from typing import Optional

import click

from src.client import LinearClient

logger = logging.getLogger(__name__)


@click.command()
@click.argument("query")
@click.option("--limit", type=int, default=50, help="Maximum number of results")
@click.option("--token", help="Linear API token")
@click.pass_context
def search(ctx, query: str, limit: int, token: Optional[str]):
    """Search for issues in Linear."""
    try:
        # Initialize client
        client = LinearClient(api_token=token)

        # Search issues
        issues = client.search_issues(query_str=query, limit=limit)

        if not issues:
            click.echo("No issues found matching your query.")
            return

        # Display results
        click.echo(f"\nFound {len(issues)} issue(s) matching '{query}':\n")

        for issue in issues:
            click.echo(
                f"[{issue.get('identifier', 'N/A')}] {issue.get('title', 'N/A')}"
            )
            click.echo(
                f"  State: {issue.get('state', {}).get('name', 'N/A')} | Priority: {issue.get('priority', 'N/A')}"
            )
            click.echo(f"  URL: {issue.get('url', 'N/A')}")

            # Show snippet of description if available
            if issue.get("description"):
                desc = issue["description"][:100]
                if len(issue["description"]) > 100:
                    desc += "..."
                click.echo(f"  Description: {desc}")

            click.echo()

    except Exception as e:
        logger.error(f"Failed to search issues: {e}")
        click.echo(f"Error: {e}", err=True)
        ctx.exit(1)
