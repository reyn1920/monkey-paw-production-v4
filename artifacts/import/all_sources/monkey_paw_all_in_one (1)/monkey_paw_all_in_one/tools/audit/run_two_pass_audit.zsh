#!/bin/zsh
set -e
echo "Pass 1: Rule-1 scan"
python3 tools/audit/rule1_guard.py
echo "Pass 2: Quick imports"
python3 - <<'PY'mods = ["fastapi","uvicorn","pydantic","ebooklib","jinja2","yaml"]
bad = []
for m in mods:
    try: __import__(m)
    except Exception as e: bad.append((m, str(e)))
if bad:
    print("Missing modules:", bad); raise SystemExit(1)
print("Imports ok")
PY
echo "Two-pass audit passed."
