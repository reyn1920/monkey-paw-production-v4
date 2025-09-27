#!/usr/bin/env zsh
set -euo pipefail
python3 - <<'PY'
import json, urllib.request
u="http://127.0.0.1:8000/api/health"
with urllib.request.urlopen(u, timeout=5) as r:
    print(json.dumps(json.loads(r.read().decode()), indent=2))
PY
