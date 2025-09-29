#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"

# Start paste server
( "$ROOT/tools/paste_server/run_paste_server.sh" ) & echo $! > "$ROOT/.pid-paste"

# Start Vite (npm by default)
if [ -f "$ROOT/package.json" ]; then
  if command -v pnpm >/dev/null 2>&1; then PM=pnpm
  elif command -v yarn >/dev/null 2>&1; then PM=yarn
  else PM=npm
  fi
  ( cd "$ROOT" && $PM install && $PM run dev ) & echo $! > "$ROOT/.pid-web"
  echo "➡ Web: http://localhost:5173   Paste: http://127.0.0.1:5000"
else
  echo "⚠ No package.json found. Paste server still running at http://127.0.0.1:5000"
fi

wait
