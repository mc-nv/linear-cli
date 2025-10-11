import argparse
import json
import os
from pathlib import Path

from src.client import LinearClient
from src.logger import get_logger


def get_builtin_dir():
    """Get built-in templates directory."""
    return Path(__file__).parent.parent / "data" / "queries"


def get_user_dir():
    """Get user-defined templates directory from env var."""
    user_dir = os.getenv("LINEAR_CLI_USER_DATA_QUERIES")
    return Path(user_dir) if user_dir else None


def list_templates():
    """List available query templates from both user and built-in directories."""
    templates = {}
    builtin_dir = get_builtin_dir()
    user_dir = get_user_dir()

    # Load built-in templates
    if builtin_dir.exists():
        for f in builtin_dir.glob("*.graphql"):
            templates[f.stem] = "built-in"

    # Load user templates (can override built-in)
    if user_dir and user_dir.exists():
        for f in user_dir.glob("*.graphql"):
            templates[f.stem] = "user"

    return sorted(templates.keys())


def load_template(name):
    """Load a query template by name. User templates take precedence over built-in."""
    user_dir = get_user_dir()
    builtin_dir = get_builtin_dir()

    # Check user directory first
    if user_dir:
        user_template = user_dir / f"{name}.graphql"
        if user_template.exists():
            return user_template.read_text()

    # Fall back to built-in
    builtin_template = builtin_dir / f"{name}.graphql"
    if builtin_template.exists():
        return builtin_template.read_text()

    raise FileNotFoundError(
        f"Template '{name}' not found in built-in or user directories"
    )


def setup_parser(subparsers, parent_parser):
    parser = subparsers.add_parser(
        "query",
        help="Execute predefined GraphQL query templates",
        parents=[parent_parser],
    )
    parser.add_argument(
        "template", nargs="?", help="Template name to execute (or 'list' to show all)"
    )
    parser.add_argument("--json", action="store_true", help="Output raw JSON response")
    parser.set_defaults(func=execute)


def execute(args):
    logger = get_logger()

    if args.template == "list" or not args.template:
        logger.debug("Listing available templates")
        templates = list_templates()
        if not templates:
            print("No templates found")
            builtin = get_builtin_dir()
            user = get_user_dir()
            print(
                f"  Built-in dir: {builtin} {'(exists)' if builtin.exists() else '(not found)'}"
            )
            if user:
                print(
                    f"  User dir: {user} {'(exists)' if user.exists() else '(not found)'}"
                )
            return 1
        print("Available templates:")
        for tmpl in templates:
            print(f"  - {tmpl}")
        user_dir = get_user_dir()
        if user_dir and user_dir.exists():
            print(f"\nUser templates: {user_dir}")
        print(f"Built-in templates: {get_builtin_dir()}")
        return 0

    try:
        logger.debug(f"Loading template: {args.template}")
        query = load_template(args.template)
        logger.info(f"Executing template: {args.template}")

        client = LinearClient(token=args.token)
        result = client.execute_query(query)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(json.dumps(result.get("data", result), indent=2))
        return 0
    except FileNotFoundError as e:
        logger.error(f"Template not found: {args.template}")
        print(f"✗ {e}")
        print(f"Available templates: {', '.join(list_templates())}")
        return 1
    except Exception as e:
        logger.error(f"Error executing query: {e}")
        print(f"✗ Error: {e}")
        return 1
