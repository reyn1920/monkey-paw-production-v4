#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BACKUP="$ROOT/.phoenix_backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP"
rsync -a --exclude ".git" "$ROOT/" "$BACKUP/"
echo "[phoenix] backup at $BACKUP"
