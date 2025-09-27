#!/usr/bin/env bash
set -euo pipefail
export SCAN_ROOT="${1:-.}"
python3 tools/dbsheet_scan.py
echo
echo "== Output files =="
ls -lh out/db_inventory.json out/sheets_inventory.json out/dbsheet_inventory.csv out/next_steps.txt 2>/dev/null || true
