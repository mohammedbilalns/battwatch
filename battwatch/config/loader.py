import tomllib
from pathlib import Path

DEFAULT_USER_CONFIG = Path.home() / ".config" / "battwatch" / "config.toml"
DEFAULT_SYSTEM_CONFIG = Path("/etc/battwatch/config.toml")  # for system-wide

def load_config():
    # Check if config file exists 
    if DEFAULT_USER_CONFIG.exists():
        path = DEFAULT_USER_CONFIG
    elif DEFAULT_SYSTEM_CONFIG.exists():
        path = DEFAULT_SYSTEM_CONFIG
    else:
        # fallback default config
        import importlib.resources
        with importlib.resources.open_text("battwatch.config", "default_config.toml") as f:
            return tomllib.load(f)
    with open(path, "rb") as f:
        return tomllib.load(f)