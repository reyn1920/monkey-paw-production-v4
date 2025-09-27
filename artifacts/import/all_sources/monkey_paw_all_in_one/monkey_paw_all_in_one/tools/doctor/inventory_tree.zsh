#!/bin/zsh
set -e
ROOT=${1:-.}
OUT=${2:-reports/INVENTORY.txt}
mkdir -p "$(dirname "$OUT")"
find "$ROOT" -type f -print0 | xargs -0 stat -f "%N|%z" | sort > "$OUT"
echo "OK"
