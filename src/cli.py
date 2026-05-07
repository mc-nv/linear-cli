import argparse
import sys

from src.commands import ping, query
from src.config import apply_config_to_env
from src.logger import setup_logger


def main():
    # Load config from ~/.config/linear/user/conf.json (env vars take precedence)
    apply_config_to_env()

    # Parent parser with common arguments shared by all subcommands
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument(
        "--token",
        help="Linear API token (or use LINEAR_CLI_TOKEN env var or config file)",
    )
    parent_parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug output (or set LINEAR_CLI_LOG_DIR for file logging)",
    )

    parser = argparse.ArgumentParser(
        prog="linear",
        description="CLI for Linear API",
        epilog="Configuration: ~/.config/linear/user/conf.json (override with LINEAR_CLI_CONFIG; supports multiple paths separated by os.pathsep, later paths override earlier ones)",
        parents=[parent_parser],
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    ping.setup_parser(subparsers, parent_parser)
    query.setup_parser(subparsers, parent_parser)
    args = parser.parse_args()

    # Setup logging based on --debug flag and LINEAR_CLI_LOG_DIR env var
    setup_logger(debug=args.debug)

    if not args.command or not hasattr(args, "func"):
        parser.print_help()
        return 1
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
