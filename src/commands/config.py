import os

from src.config import get_env_snapshot, get_file_status, load_config_with_sources


def setup_parser(subparsers, parent_parser):
    parser = subparsers.add_parser(
        "config",
        help="Inspect resolved configuration and its sources",
        parents=[parent_parser],
    )
    parser.add_argument(
        "action",
        nargs="?",
        default="get",
        choices=["get"],
        help="Action to perform (default: get)",
    )
    parser.set_defaults(func=execute)


def _redact(key, value):
    if "TOKEN" in key.upper() and value:
        if len(value) <= 8:
            return "***"
        return f"{value[:4]}...{value[-4:]}"
    return value


def execute(args):
    file_config, file_sources = load_config_with_sources()
    env_snapshot = get_env_snapshot()
    file_status = get_file_status()

    keys = set(file_config.keys())
    keys.update(k for k in os.environ if k.startswith("LINEAR_CLI_"))
    keys.update(k for k in env_snapshot if k.startswith("LINEAR_CLI_"))

    print("Resolved configuration:")
    if not keys:
        print("  (no LINEAR_CLI_* values set)")
    for k in sorted(keys):
        value = os.environ.get(k, "")
        if k in env_snapshot:
            source = "env"
        elif k in file_sources:
            source = f"file: {file_sources[k]}"
        else:
            source = "unset"
        print(f"  {k} = {_redact(k, value)}  ({source})")

    print("\nConfig files (in load order, later wins):")
    if not file_status:
        print("  (none — LINEAR_CLI_CONFIG is empty)")
    for path, status in file_status:
        print(f"  - {path}  [{status}]")

    cli_config_env = env_snapshot.get("LINEAR_CLI_CONFIG")
    print("\nLINEAR_CLI_CONFIG env var:")
    print(
        f"  {cli_config_env if cli_config_env is not None else '(unset, using default)'}"
    )

    return 0
