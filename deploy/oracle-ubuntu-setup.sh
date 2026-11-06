#!/usr/bin/env bash
# OpenSTEM Telegram Bot - initial installation on an Ubuntu OCI Always Free VM.
# Run: sudo bash deploy/oracle-ubuntu-setup.sh
# Do not supply Telegram credentials to this script.
set -Eeuo pipefail

APP_DIR="/opt/openstem-telegram-bot"
SERVICE_USER="openstembot"
SERVICE_FILE="/etc/systemd/system/openstem-bot.service"
ENV_FILE="/etc/openstem-bot.env"
REPO_URL="https://github.com/karim8siam/openstemtg.git"

if [[ "$(id -u)" -ne 0 ]]; then
  echo "Run as root: sudo bash deploy/oracle-ubuntu-setup.sh" >&2
  exit 1
fi

if ! command -v apt-get >/dev/null 2>&1; then
  echo "This script supports Ubuntu/Debian-based instances only." >&2
  exit 1
fi

if [[ -e "$APP_DIR" ]]; then
  echo "Installation directory $APP_DIR already exists. Refusing to overwrite it or its database." >&2
  exit 1
fi

export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y --no-install-recommends ca-certificates git python3 python3-venv python3-pip

if ! id "$SERVICE_USER" >/dev/null 2>&1; then
  useradd --system --no-create-home --shell /usr/sbin/nologin "$SERVICE_USER"
fi

git clone --depth 1 "$REPO_URL" "$APP_DIR"
if [[ ! -s "$APP_DIR/data/openstem.db" ]]; then
  echo "Missing bundled SQLite database. Stopping installation." >&2
  exit 1
fi

chown -R "$SERVICE_USER:$SERVICE_USER" "$APP_DIR"
runuser -u "$SERVICE_USER" -- python3 -m venv "$APP_DIR/.venv"
runuser -u "$SERVICE_USER" -- "$APP_DIR/.venv/bin/python" -m pip install --disable-pip-version-check -r "$APP_DIR/requirements.txt"
runuser -u "$SERVICE_USER" -- "$APP_DIR/.venv/bin/python" -m compileall -q "$APP_DIR/bot"

# Only a root-readable placeholder. User must add freshly rotated BOT_TOKEN manually.
if [[ ! -e "$ENV_FILE" ]]; then
  install -m 0600 -o root -g root /dev/null "$ENV_FILE"
fi

cat > "$SERVICE_FILE" <<'UNIT'
[Unit]
Description=OpenSTEM Telegram Bot (long polling)
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=openstembot
Group=openstembot
WorkingDirectory=/opt/openstem-telegram-bot
EnvironmentFile=/etc/openstem-bot.env
Environment=PYTHONUNBUFFERED=1
ExecStart=/opt/openstem-telegram-bot/.venv/bin/python -m bot.main
Restart=always
RestartSec=10
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=full
ProtectHome=true
UMask=0077

[Install]
WantedBy=multi-user.target
UNIT

chmod 0644 "$SERVICE_FILE"
systemctl daemon-reload
systemctl enable openstem-bot.service

echo
echo "Installed OpenSTEM bot. Service is deliberately NOT started."
echo "1. Rotate the previously exposed token using Telegram @BotFather."
echo "2. Add BOT_TOKEN=<new token> securely to $ENV_FILE:"
echo "       sudo nano $ENV_FILE"
echo "3. Start bot: sudo systemctl start openstem-bot"
echo "4. Verify: sudo systemctl status openstem-bot --no-pager"
echo "5. Logs: sudo journalctl -u openstem-bot -n 80 --no-pager"
echo "No inbound HTTP port needs to be opened for Telegram long polling."
