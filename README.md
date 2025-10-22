# Battwatch - Battery Notification Daemon

**Battwatch** is a lightweight battery monitoring and notification daemon for Linux.  
It notifies you when your battery is low, critical, or fully charged.

---

## Features

- Notifies on **low**, **critical**, and **full** battery levels.
- Configurable thresholds and messages via a TOML configuration file.
- Lightweight, polling-based monitoring.
- User-level systemd service for automatic startup.

---

## Installation

1. **Clone or download** the repository and navigate to the project folder:
   ```bash
   git clone https://github.com/mohammedbilalns/battwatch.git
   cd battwatch
   ```

2. **Run the installer script**:
   ```bash
   ./install.sh
   ```

   This will:
   - Copy the package to `/opt/battwatch`.
   - Install a launcher script at `/usr/bin/battwatch`.
   - Copy a user-level systemd service to `$HOME/.config/systemd/user/battwatch.service`.
   - Copy the default configuration file to the package directory.

---

## Running Battwatch

After installation, you can run Battwatch in one of two ways:

1. **Enable the user-level systemd service**:
   ```bash
   systemctl --user enable --now battwatch.service
   ```

   This will automatically start Battwatch on login 
2. **Launch manually in your WM/compositor startup**:
   Add the following line to your startup script:
   eg: for hyprland
   ```bash
   exec-once battwatch
   ```

---

## Configuration

- The default configuration file is located at:
  ```
  /opt/battwatch/battwatch/config/default_config.toml
  ```

- You can override the defaults by creating a custom config in:
  ```
  ~/.config/battwatch/config.toml
  ```

- Example options:
  ```toml
  [daemon]
  poll_interval = 60  # seconds

  [notifications]
  low_threshold = 25
  critical_threshold = 10
  notify_full = true
  full_threshold = 90

  [messages]
  low = "Battery low: {percent}% remaining"
  critical = "Battery critical: {percent}%! Plug in now."
  full = "Battery full: You can unplug the charger"
  ```

- After modifying the configuration, **restart the service**:
  ```bash
  systemctl --user restart battwatch.service
  ```

---

## Uninstallation

To uninstall Battwatch, run:

```bash
./install.sh --uninstall
```
---


## Dependencies

- Python 3.11+
- `psutil` Python library
- `notify-send`

---

## License

MIT License

