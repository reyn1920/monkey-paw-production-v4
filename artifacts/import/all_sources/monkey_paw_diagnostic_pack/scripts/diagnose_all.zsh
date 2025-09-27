#!/bin/zsh
set -euo pipefail
ROOT="${1:-.}"
TS=$(date +"%Y%m%d_%H%M%S")
OUT="${ROOT}/reports/diagnostic_${TS}"
mkdir -p "${OUT}"
echo "== Monkey Paw Diagnostic =="
echo "Root: ${ROOT}"
echo "Out:  ${OUT}"
python3 "$(dirname "$0")/static_route_scan.py" "${ROOT}" > "${OUT}/routes_static.json" || true
python3 "$(dirname "$0")/scan_jobs.py"         "${ROOT}" > "${OUT}/jobs.json" || true
python3 "$(dirname "$0")/scan_db.py"           "${ROOT}" > "${OUT}/db.json" || true
python3 "$(dirname "$0")/scan_faiss.py"        "${ROOT}" > "${OUT}/faiss.json" || true
python3 "$(dirname "$0")/scan_config.py"       "${ROOT}" > "${OUT}/config.json" || true
python3 "$(dirname "$0")/scan_addon.py"        "${ROOT}" > "${OUT}/addon_matches.json" || true
export PYTHONPATH="${ROOT}:${PYTHONPATH:-}"
python3 "$(dirname "$0")/runtime_route_scan.py" > "${OUT}/routes_runtime.json" || true
cat > "${OUT}/SUMMARY.md" <<'MD'
# Monkey Paw — Diagnostic Summary
This folder contains:
- routes_static.json — regex-based route mapping
- routes_runtime.json — attempted runtime route enumeration (MP_APP_SPEC=app.main:app)
- jobs.json — job scheduling and task hints
- db.json — SQLModel/SQLite indicators
- faiss.json — FAISS references and index files
- config.json — config files and likely feature flag files
- addon_matches.json — locations of no-code coder stack files
Notes:
- "routes_runtime.json" requires an importable app; set MP_APP_SPEC if not app.main:app.
- All scans are read-only, stdlib-only.
MD
echo ""; echo "✅ Diagnostic complete. See ${OUT}"
