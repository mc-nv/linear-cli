import argparse
import json
import os
from pathlib import Path

from src.client import LinearClient


def get_data_dir():
    """Get data directory from env var or default package location."""
    user_dir = os.getenv("LINEAR_USER_DATA_QUERIES")
    if user_dir:
        return Path(user_dir)
    return Path(__file__).parent.parent.parent / "data" / "queries"


def list_templates():
    """List available query templates."""
    data_dir = get_data_dir()
    if not data_dir.exists():
        return []
    return sorted([f.stem for f in data_dir.glob("*.graphql")])


def load_template(name):
    """Load a query template by name."""
    data_dir = get_data_dir()
    template_path = data_dir / f"{name}.graphql"
    if not template_path.exists():
        raise FileNotFoundError(f"Template '{name}' not found in {data_dir}")
    return template_path.read_text()


def setup_parser(subparsers):
    parser = subparsers.add_parser(
        "query", help="Execute predefined GraphQL query templates"
    )
    parser.add_argument(
        "template", nargs="?", help="Template name to execute (or 'list' to show all)"
    )
    parser.add_argument("--json", action="store_true", help="Output raw JSON response")
    parser.set_defaults(func=execute)


def execute(args):
    if args.template == "list" or not args.template:
        templates = list_templates()
        if not templates:
            print(f"No templates found in {get_data_dir()}")
            return 1
        print("Available templates:")
        for tmpl in templates:
            print(f"  - {tmpl}")
        return 0

    try:
        client = LinearClient(token=args.token)
        query = load_template(args.template)
        result = client.execute_query(query)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(json.dumps(result.get("data", result), indent=2))
        return 0
    except FileNotFoundError as e:
        print(f"✗ {e}")
        print(f"Available templates: {', '.join(list_templates())}")
        return 1
    except Exception as e:
        print(f"✗ Error: {e}")
        return 1
