#!/bin/zsh
# Dedup by hash; copy PNG/JPG into assets/thumbnails
set -e
SRC=${1:-~/Pictures}
DST=assets/thumbnails
LOG=reports/IMPORT_THUMBNAILS.log
mkdir -p "$DST" reports
: > "$LOG"
for f in $(find "$SRC" -type f \( -iname "*.png" -o -iname "*.jpg" -o -iname "*.jpeg" \)); do
  h=$(shasum -a 256 "$f" | awk '{print $1}')
  out="$DST/$h.${f##*.}"
  if [ ! -f "$out" ]; then
    cp "$f" "$out"
    echo "$(basename "$f") -> $(basename "$out")" >> "$LOG"
  fi
done
echo "Done. See $LOG"
