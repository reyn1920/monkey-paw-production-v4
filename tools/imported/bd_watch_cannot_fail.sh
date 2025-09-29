#!/usr/bin/env bash
set -euo pipefail
ROOT="${1:-.}"
if command -v fswatch >/dev/null 2>&1; then
  echo "[watch] using fswatch"
  fswatch -o "$ROOT" | while read -r _; do
    echo "[watch] change detected"; python3 tools/cannot_fail.py --root "$ROOT" --passes 6 || true
  done
else
  echo "[watch] using simple polling"
  LAST=""
  while true; do
    CUR="$(find "$ROOT" -type f -not -path "*/.git/*" -exec md5 -q {} \; 2>/dev/null | md5)"
    if [[ "$CUR" != "$LAST" ]]; then
      echo "[watch] change detected"
      python3 tools/cannot_fail.py --root "$ROOT" --passes 6 || true
      LAST="$CUR"
    fi
    sleep 3
  done
fi
