import tomllib
from pathlib import Path

DEFAULT_PATH = Path.home() / ".config" / "battwatch" / "config.toml"

def load_config(path: Path = DEFAULT_PATH):
  if not path.exists():
    raise FileNotFoundError(f"Configuratino file not found: {path}")
  with open(path, "rb") as f:
    return tomllib.load(f)