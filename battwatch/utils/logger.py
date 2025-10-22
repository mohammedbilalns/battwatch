import logging
from pathlib import Path

LOG_FILE = Path.home() / ".local/share/battwatch/daemon.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
)

def log(msg: str):
    print(msg)
    logging.info(msg)
