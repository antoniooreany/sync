"""Configuration utilities for the automation toolkit."""
import os
import re
import json
from pathlib import Path
from typing import Any

_ENV_PATTERN = re.compile(r"\$\{([A-Z0-9_]+)\}")

class ConfigError(Exception):
    """Raised when config is missing required fields or env vars."""

def expand_env(value: Any) -> Any:
    """Recursively expand ${ENV_VAR} strings in configuration data."""
    if isinstance(value, str):
        def repl(match: re.Match) -> str:
            name = match.group(1)
            if name not in os.environ:
                raise ConfigError(f"Environment variable '{name}' is not set (required by config)")
            return os.environ[name]
        return _ENV_PATTERN.sub(repl, value)
    if isinstance(value, dict):
        return {k: expand_env(v) for k, v in value.items()}
    if isinstance(value, list):
        return [expand_env(v) for v in value]
    return value

def load_json_config(path: str | Path) -> dict[str, Any]:
    """Load JSON config and expand environment variables."""
    raw_text = Path(path).read_text(encoding="utf-8")
    raw = json.loads(raw_text)
    return expand_env(raw)
