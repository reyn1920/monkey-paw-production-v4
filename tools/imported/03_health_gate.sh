#!/usr/bin/env bash
set -euo pipefail
URL="${1:-http://localhost:8000/health}"
TRIES=30
for i in $(seq 1 $TRIES); do
  if command -v curl >/dev/null 2>&1; then
    if curl -fsS "$URL" >/dev/null 2>&1; then echo "[health] ok"; exit 0; fi
  else
    python3 - <<'PY' "$URL"
import sys, json, urllib.request
url = sys.argv[1]
try:
    with urllib.request.urlopen(url, timeout=2) as r:
        if r.status == 200: print("[health] ok")
        else: raise SystemExit(1)
except Exception:
    raise SystemExit(1)
PY
  fi
  sleep 1
done
echo "[health] timeout"; exit 1
