import json
import os
from pathlib import Path

_env_snapshot = None
_file_status = []


def _config_paths():
    """Paths from LINEAR_CLI_CONFIG (os.pathsep-separated) or the default."""
    env = os.getenv("LINEAR_CLI_CONFIG")
    if env is None:
        return [Path.home() / ".config" / "linear" / "user" / "conf.json"]
    return [Path(p).expanduser() for p in env.split(os.pathsep) if p]


def load_config_with_sources():
    """Load and merge config files. Later paths override earlier ones.
    Returns (merged_dict, sources_dict) where sources_dict maps each key to
    the Path of the file that last set it. Records each path's load status
    in the module-level _file_status list."""
    global _file_status
    merged = {}
    sources = {}
    _file_status = []
    for path in _config_paths():
        if not path.exists():
            _file_status.append((path, "missing"))
            continue
        try:
            with open(path) as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            _file_status.append((path, f"invalid: {e}"))
            continue
        _file_status.append((path, "loaded"))
        for k, v in data.items():
            merged[k] = v
            sources[k] = path
    return merged, sources


def load_config():
    """Load and merge config files. Later paths override earlier ones."""
    merged, _ = load_config_with_sources()
    return merged


def apply_config_to_env():
    """Apply config values to env vars. Actual env vars take precedence."""
    global _env_snapshot
    _env_snapshot = dict(os.environ)
    config = load_config()
    for key, value in config.items():
        if key not in os.environ:
            os.environ[key] = str(value)


def get_env_snapshot():
    """Snapshot of os.environ taken before apply_config_to_env() mutated it."""
    return dict(_env_snapshot) if _env_snapshot is not None else dict(os.environ)


def get_file_status():
    """List of (path, status) tuples from the most recent load."""
    return list(_file_status)
