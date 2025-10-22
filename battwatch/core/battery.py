import psutil 

def get_battery_status():
  battery = psutil.sensors_battery()
  if not battery: 
    return None
  return {
    "percent": battery.percent,
    "plugged": battery.power_plugged,
    "secs_left": battery.secsleft
  }