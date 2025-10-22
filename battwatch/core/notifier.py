import subprocess

def send_notification(title: str , message: str):
  try:
    subprocess.run(
      ["notify-send", title, message],
      check=True
    )
  except Exception as e:
    print(f"[Notifier Error] {e}")