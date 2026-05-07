import json
import os
from pathlib import Path


def _config_paths():
    """Paths from LINEAR_CLI_CONFIG (os.pathsep-separated) or the default."""
    env = os.getenv("LINEAR_CLI_CONFIG")
    if env is None:
        return [Path.home() / ".config" / "linear" / "user" / "conf.json"]
    return [Path(p) for p in env.split(os.pathsep) if p]


def load_config():
    """Load and merge config files. Later paths override earlier ones."""
    merged = {}
    for path in _config_paths():
        if not path.exists():
            continue
        try:
            with open(path) as f:
                merged.update(json.load(f))
        except (json.JSONDecodeError, IOError):
            continue
    return merged


def apply_config_to_env():
    """Apply config values to env vars. Actual env vars take precedence."""
    config = load_config()
    for key, value in config.items():
        if key not in os.environ:
            os.environ[key] = str(value)
