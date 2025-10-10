import argparse
import sys

from src.commands import ping, query


def main():
    parser = argparse.ArgumentParser(prog="linear", description="CLI for Linear API")
    parser.add_argument(
        "--token", help="Linear API token (or use LINEAR_TOKEN env var)"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    ping.setup_parser(subparsers)
    query.setup_parser(subparsers)
    args = parser.parse_args()
    if not args.command or not hasattr(args, "func"):
        parser.print_help()
        return 1
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
