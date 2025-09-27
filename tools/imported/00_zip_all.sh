#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/sites.env"

for entry in "${SITES[@]}"; do
  IFS="::" read -r RAW_PATH RAW_REPO <<< "$entry"
  SITE_PATH="$(echo "$RAW_PATH" | xargs)"
  SAFE_NAME="$(echo "$RAW_REPO" | xargs)"
  if [[ -d "$SITE_PATH" ]]; then
    echo "Zipping $SITE_PATH -> ${SAFE_NAME}.zip"
    (cd "$SITE_PATH" && zip -qr "../${SAFE_NAME}.zip" .)
  else
    echo "Skip: $SITE_PATH not found"
  fi
done
