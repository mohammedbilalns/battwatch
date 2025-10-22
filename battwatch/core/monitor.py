import time 
from battwatch.core.battery import get_battery_status
from battwatch.core.notifier import send_notification
from battwatch.utils.logger import log

def run_monitor(config):
  # Extract configuration values for notifications and polling
  low_threshold = config["notifications"]["low_threshold"]
  critical_threshold = config["notifications"]["critical_threshold"]
  notify_full = config["notifications"].get("notify_full", True)
  poll_interval = config["daemon"]["poll_interval"]
  messages = config["messages"]

  # Keep track of whether a notification has already been sent
  last_state = {"low": False, "critical":False, "full": False}

  log("Starting battery monitor loop...")

  while True: 
    # Get current battery status
    status = get_battery_status()
    if not status:
      # Exit the loop if no battery is detected
      log("No battery detected.")
      break

    percent = status["percent"]
    plugged = status["plugged"]

    if not plugged:
      if percent <= critical_threshold and not last_state["critical"]:
        # Critical battery level reached
        send_notification("Battery Critical", messages["critical"].format(percent = percent))
        last_state["critical"] = True
        last_state["low"] = True
      elif percent <= low_threshold and not last_state["low"]:
        # Low battery level reached
        send_notification("Battery Low", messages["low"].format(percent=percent))
        last_state["low"] = True
    else:
      # Reset low flags when plugged in 
      last_state["low"] = last_state["critical"] = False
      if notify_full and percent >=95 and not last_state['full']:
        # Battery is nearly full, send notification
        send_notification("Battery Full", messages["Full"].format(percent=percent))
        last_state["full"] = True
      elif percent <95:
        last_state['full'] = False
      
    time.sleep(poll_interval)

  
