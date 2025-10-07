"""Create command for linear-cli."""

import logging
from typing import Optional

import click

from src.client import LinearClient
from src.utils import format_issue, get_template

logger = logging.getLogger(__name__)


@click.command()
@click.option("--title", "-t", required=True, help="Issue title")
@click.option("--description", "-d", help="Issue description")
@click.option("--team-id", help="Team ID")
@click.option("--priority", type=int, help="Priority (0-4)")
@click.option("--labels", help="Comma-separated list of label IDs")
@click.option("--template", help="Template name to use")
@click.option("--token", help="Linear API token")
@click.pass_context
def create(
    ctx,
    title: str,
    description: Optional[str],
    team_id: Optional[str],
    priority: Optional[int],
    labels: Optional[str],
    template: Optional[str],
    token: Optional[str],
):
    """Create a new issue in Linear."""
    try:
        # Get template if specified
        template_data = get_template(template) if template else None

        # Apply template
        if template_data:
            logger.debug(f"Using template: {template}")

            # Format title and description with template
            if "{title}" in template_data.get("title", ""):
                title = template_data["title"].replace("{title}", title)

            if description and "{description}" in template_data.get("description", ""):
                description = template_data["description"].replace(
                    "{description}", description
                )
            elif not description and template_data.get("description"):
                description = template_data["description"].replace("{description}", "")

            # Use template priority if not specified
            if priority is None and template_data.get("priority"):
                priority = template_data["priority"]

            # Use template labels if not specified
            if not labels and template_data.get("labels"):
                labels = ",".join(template_data["labels"])

        # Parse labels
        label_list = [l.strip() for l in labels.split(",")] if labels else None

        # Get team ID from environment if not provided
        if not team_id:
            from src.utils import get_config_value

            team_id = get_config_value("TEAM_ID")

        # Initialize client
        client = LinearClient(api_token=token)

        # Create issue
        issue = client.create_issue(
            title=title,
            description=description,
            team_id=team_id,
            priority=priority,
            labels=label_list,
        )

        # Display result
        click.echo("\n✓ Issue created successfully!\n")
        click.echo(format_issue(issue))

    except Exception as e:
        logger.error(f"Failed to create issue: {e}")
        click.echo(f"Error: {e}", err=True)
        ctx.exit(1)
