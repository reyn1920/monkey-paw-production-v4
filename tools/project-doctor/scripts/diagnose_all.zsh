#!/usr/bin/env zsh
set -euo pipefail
ROOT="${1:-.}"
OUT="$ROOT/reports/diagnostic_$(date -u +%Y%m%d_%H%M%S)"
mkdir -p "$OUT"
python3 "$(dirname "$0")/static_route_scan.py" "$ROOT" > "$OUT/routes_static.json" || true
python3 "$(dirname "$0")/runtime_route_scan.py" "$ROOT" > "$OUT/routes_runtime.json" || true
python3 "$(dirname "$0")/scan_jobs.py" "$ROOT" > "$OUT/jobs.json" || true
python3 "$(dirname "$0")/scan_db.py" "$ROOT" > "$OUT/db.json" || true
python3 "$(dirname "$0")/scan_faiss.py" "$ROOT" > "$OUT/faiss.json" || true
python3 "$(dirname "$0")/scan_config.py" "$ROOT" > "$OUT/config.json" || true
python3 "$(dirname "$0")/scan_addon.py" "$ROOT" > "$OUT/addon_matches.json" || true
cat > "$OUT/SUMMARY.md" <<MD
# Diagnostic Summary
Artifacts:
- routes_static.json
- routes_runtime.json
- jobs.json
- db.json
- faiss.json
- config.json
- addon_matches.json
MD
echo "$OUT"
