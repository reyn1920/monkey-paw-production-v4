#!/bin/zsh
set -e
python3 - <<'PY'
import json, urllib.request
with urllib.request.urlopen("http://127.0.0.1:8000/api/health", timeout=5) as r:
    data = json.loads(r.read().decode())
assert data.get("ok") is True
print("✅ Live health ok:", data)
PY
