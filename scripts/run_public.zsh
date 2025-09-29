#!/bin/zsh
set -e

# Resolve project root (this script is in scripts/)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

# Paths and logs
VENV_DIR=".venv_monkeypawv4"
APP_LOG="/tmp/monkey_paw_v4_uvicorn.log"
TUNNEL_LOG="/tmp/cloudflared_monkeypaw.log"
APP_URL="http://127.0.0.1:8000"

# Ensure virtual environment
if [ ! -d "$VENV_DIR" ]; then
  python3 -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"
python -m pip install --upgrade pip setuptools wheel >/dev/null
python -m pip install -r requirements.txt >/dev/null

# Start app server if not already listening on 8000
if ! lsof -ti:8000 >/dev/null 2>&1; then
  ( uvicorn app.main:app --host 127.0.0.1 --port 8000 --loop uvloop --http httptools --reload ) >"$APP_LOG" 2>&1 &
  echo "Started uvicorn (logs: $APP_LOG)"
else
  echo "Uvicorn already running on 8000; leaving it as-is (logs: $APP_LOG)"
fi

# Start Cloudflare Quick Tunnel if not already running
if ! pgrep -f "cloudflared tunnel --url" >/dev/null 2>&1; then
  ( cloudflared tunnel --url "$APP_URL" --logfile "$TUNNEL_LOG" --no-autoupdate ) >/dev/null 2>&1 &
  echo "Started cloudflared (logs: $TUNNEL_LOG)"
else
  echo "cloudflared tunnel already running; leaving it as-is (logs: $TUNNEL_LOG)"
fi

# Wait briefly for URL to appear in the log
sleep 2
PUBLIC_URL=$(grep -Eo "https://[a-z0-9-]+\.trycloudflare\.com" "$TUNNEL_LOG" | tail -n 1 || true)
if [ -n "$PUBLIC_URL" ]; then
  echo "Public URL: $PUBLIC_URL"
  # Open on macOS if available
  if [[ "$OSTYPE" == darwin* ]]; then
    open "$PUBLIC_URL" || true
  fi
else
  echo "Public URL not found yet. Check logs: $TUNNEL_LOG"
fi

# Health check
set +e
if command -v curl >/dev/null 2>&1; then
  echo "Health: $(curl -s "$APP_URL/api/health")"
fi
