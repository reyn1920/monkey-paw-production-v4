#!/bin/zsh
# Usage: zsh tools/importers/import_writing.zsh ~/Documents/Writing
set -e
SRC=${1:-~/Documents}
DST=artifacts/library/writing
LOG=reports/IMPORT_WRITING.log
mkdir -p "$DST" reports
echo "Import from: $SRC" > "$LOG"
find "$SRC" -type f \( -iname "*.txt" -o -iname "*.md" -o -iname "*.docx" -o -iname "*.rtf" \) -print0 |   xargs -0 -I{} bash -c 'f="{}"; base=$(basename "$f"); cp -n "$f" "'"$DST"'"/"$base" 2>/dev/null || true; echo "$base" >> "'"$LOG"'"'
echo "Done. See $LOG"
