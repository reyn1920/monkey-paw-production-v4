#!/bin/zsh
# Copy marketing playbooks/templates (md/markdown) into assets/marketing
set -e
SRC=${1:-~/Documents}
DST=assets/marketing
mkdir -p "$DST"
find "$SRC" -type f \( -iname "*.md" -o -iname "*.markdown" \) -maxdepth 2 -print0 |   xargs -0 -I{} cp -n "{}" "$DST"/ 2>/dev/null || true
echo "Imported to $DST"
