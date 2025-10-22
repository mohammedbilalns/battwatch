from battwatch.config.loader import load_config
from battwatch.core.monitor import run_monitor
from battwatch.utils.logger import log

def main():
    try:
        config = load_config()
        log("Configuration loaded successfully.")
        run_monitor(config)
    except Exception as e:
        log(f"Daemon error: {e}")

if __name__ == "__main__":
    main()
