#!/bin/zsh
set -e
echo "== Live Test =="
BASE="http://127.0.0.1:8000"
python3 - <<'PY'
import json, urllib.request, time
BASE="http://127.0.0.1:8000"
def get(path):
    with urllib.request.urlopen(BASE+path, timeout=5) as r:
        return r.getcode(), json.loads(r.read().decode())
code, data = get("/api/health"); assert code==200 and data.get("ok"), "/api/health failed"
print("health ok:", data)
print("✅ Live test passed")
PY
