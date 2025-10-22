#!/usr/bin/env bash

# --- Paths ---
PACKAGE_SRC="$(pwd)/battwatch"
INSTALL_DIR="/opt/battwatch"
BIN_LAUNCHER="/usr/bin/battwatch"
USER_SERVICE_DIR="$HOME/.config/systemd/user"  # User service location
CONFIG_DIR="/etc/battwatch"


set -e

usage() {
    echo "Usage: $0 [--uninstall]"
    exit 1
}

if [[ "$1" == "--uninstall" ]]; then
    echo "Uninstalling battwatch..."
    systemctl --user stop battwatch.service || true
    systemctl --user disable battwatch.service || true
    sudo rm -f "$BIN_LAUNCHER"
    sudo rm -rf "$INSTALL_DIR"
    sudo rm -rf "$CONFIG_DIR"
    rm -f "$USER_SERVICE_DIR/battwatch.service"
    systemctl --user daemon-reload
    echo "Uninstalled successfully."
    exit 0
fi

echo "Installing battwatch system-wide..."

# --- Copy package ---
sudo mkdir -p "$INSTALL_DIR"
sudo cp -r "$PACKAGE_SRC" "$INSTALL_DIR/"
echo "Copied package to $INSTALL_DIR"

# --- Ensure default config exists in package ---
sudo mkdir -p "$CONFIG_DIR"
sudo cp configs/config.toml "$CONFIG_DIR/config.toml"
echo "Copied default config to $CONFIG_DIR/config.toml"

# --- Create launcher script ---
echo "Creating launcher script at $BIN_LAUNCHER"
sudo tee "$BIN_LAUNCHER" > /dev/null <<'EOF'
#!/usr/bin/env bash
export PYTHONPATH=/opt/battwatch:$PYTHONPATH
exec python3 -m battwatch.main
EOF
sudo chmod +x "$BIN_LAUNCHER"

# --- Install user service ---
echo "Installing user service..."
mkdir -p "$USER_SERVICE_DIR"
cp systemd/battwatch.service "$USER_SERVICE_DIR/battwatch.service"
systemctl --user daemon-reload

echo "Installation complete!"
echo "To run Battwatch, either enable the user-level systemd service:"
echo "  systemctl --user enable --now battwatch.service"
echo "or launch it directly in your WM/compositor startup"
