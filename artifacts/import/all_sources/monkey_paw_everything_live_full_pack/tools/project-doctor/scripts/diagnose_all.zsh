#!/usr/bin/env zsh
set -euo pipefail
ROOT="${1:-.}"
OUT="$ROOT/reports/diagnostic_$(date -u +%Y%m%d_%H%M%S)"
mkdir -p "$OUT"
echo '{"routes":[]}' > "$OUT/routes_static.json"
echo '{"db":[]}' > "$OUT/db.json"
cat > "$OUT/SUMMARY.md" <<MD
# Diagnostic Summary
- routes_static.json
- db.json
MD
echo "$OUT"
