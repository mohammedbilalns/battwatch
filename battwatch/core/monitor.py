import time 
import math
from battwatch.core.battery import get_battery_status
from battwatch.core.notifier import send_notification
from battwatch.utils.logger import log

def run_monitor(config):
    # Extract configuration values for notifications and polling
    low_threshold = config["notifications"]["low_threshold"]
    critical_threshold = config["notifications"]["critical_threshold"]
    full_threshold = config["notifications"].get("full_threshold", 95)
    notify_full = config["notifications"].get("notify_full", True)
    poll_interval = config["daemon"]["poll_interval"]
    messages = config["messages"]

    log("Starting battery monitor loop...")

    # Get initial battery state
    status = get_battery_status()
    if not status:
        log("No battery detected at startup.")
        return

    percent = math.floor(status["percent"])
    plugged = status["plugged"]

    # track previous state 
    last_state = {
        "low": percent <= low_threshold,
        "critical": percent <= critical_threshold,
        "full": plugged and percent >= full_threshold,
    }

    log(f"Initial battery state: {percent}% | Plugged: {plugged}")

    # Start monitor loop
    while True:
        try:
            status = get_battery_status()
            if not status:
                log("No battery detected.")
                break

            percent = math.floor(status["percent"])
            plugged = status["plugged"]

            if not plugged:
                if percent <= critical_threshold and not last_state["critical"]:
                    send_notification("Battery Critical", messages["critical"].format(percent=percent))
                    last_state["critical"] = True
                    last_state["low"] = True
                elif percent <= low_threshold and not last_state["low"]:
                    send_notification("Battery Low", messages["low"].format(percent=percent))
                    last_state["low"] = True
            else:
                # Reset low flags when plugged in
                last_state["low"] = last_state["critical"] = False
                if notify_full and percent >= full_threshold and not last_state["full"]:
                    send_notification("Battery Full", messages["full"].format(percent=percent))
                    last_state["full"] = True
                elif percent < full_threshold:
                    last_state["full"] = False

            time.sleep(poll_interval)

        except KeyboardInterrupt:
            log("Battery monitor stopped by user.")
            break
        except Exception as e:
            log(f"Error in battery monitor loop: {e}")
            time.sleep(poll_interval)
