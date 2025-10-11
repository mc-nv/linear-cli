import json
import os
from pathlib import Path


def load_config():
    """Load config from LINEAR_CLI_CONFIG or ~/.config/linear/user/conf.json."""
    config_path = Path(
        os.getenv(
            "LINEAR_CLI_CONFIG",
            Path.home() / ".config" / "linear" / "user" / "conf.json",
        )
    )
    try:
        return json.load(open(config_path)) if config_path.exists() else {}
    except (json.JSONDecodeError, IOError):
        return {}


def apply_config_to_env():
    """Apply config values to env vars. Actual env vars take precedence."""
    config = load_config()
    for key, value in config.items():
        if key not in os.environ:
            os.environ[key] = str(value)
