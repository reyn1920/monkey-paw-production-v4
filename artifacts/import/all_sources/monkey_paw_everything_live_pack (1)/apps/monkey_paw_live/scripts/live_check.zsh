#!/usr/bin/env zsh
set -euo pipefail
URL="http://127.0.0.1:8000/api/health"
python3 - <<PY
import json, urllib.request, sys
u = sys.argv[1]
try:
    with urllib.request.urlopen(u, timeout=5) as r:
        data = json.loads(r.read().decode())
        ok = bool(data.get("ok"))
        print("GREEN" if ok else "YELLOW", data)
except Exception as e:
    print("RED", str(e))
    sys.exit(1)
PY
