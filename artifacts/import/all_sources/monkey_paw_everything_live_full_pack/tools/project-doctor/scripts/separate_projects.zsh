#!/usr/bin/env zsh
set -euo pipefail
ROOT="${1:-$PWD}"
OUT="$HOME/Desktop/nocode-coder-stack"
mkdir -p "$OUT"
echo "Copy-based separation to $OUT (patterns: nocode, lowcode)"
grep -ril "nocode\|lowcode" "$ROOT" | while read -r f; do
  if [[ -f "$f" ]]; then
    dest="$OUT/${f#$ROOT/}"
    mkdir -p "$(dirname "$dest")"
    cp -a "$f" "$dest"
  fi
done
echo "Separation done."
