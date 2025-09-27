#!/bin/zsh
# Simple free watchdog to keep uvicorn and cloudflared alive (non-destructive)
# Logs: /tmp/monkeypaw_watchdog.log

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

LOG="/tmp/monkeypaw_watchdog.log"
APP_LOG="/tmp/monkey_paw_v4_uvicorn.log"
TUNNEL_LOG="/tmp/cloudflared_monkeypaw.log"
VENV_DIR=".venv_monkeypawv4"
APP_URL="http://127.0.0.1:8000"

ensure_app() {
  if ! lsof -ti:8000 >/dev/null 2>&1; then
    echo "[$(date -Is)] uvicorn not running; starting" >> "$LOG"
    ( uvicorn app.main:app --host 127.0.0.1 --port 8000 --loop uvloop --http httptools --reload ) >> "$APP_LOG" 2>&1 &
  fi
}

ensure_tunnel() {
  if ! pgrep -f "cloudflared tunnel --url" >/dev/null 2>&1; then
    echo "[$(date -Is)] cloudflared not running; starting" >> "$LOG"
    ( cloudflared tunnel --url "$APP_URL" --logfile "$TUNNEL_LOG" --no-autoupdate ) >/dev/null 2>&1 &
  fi
}

# Main loop
(
  echo "[$(date -Is)] Watchdog started" >> "$LOG"
  if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
  fi
  source "$VENV_DIR/bin/activate"
  python -m pip install --upgrade pip setuptools wheel >/dev/null
  python -m pip install -r requirements.txt >/dev/null

  while true; do
    ensure_app
    ensure_tunnel
    sleep 10
  done
) &

echo "Watchdog running. Log: $LOG"
