#!/usr/bin/env zsh
set -euo pipefail
ROOT="${1:-.}"
OUT="$ROOT/reports/diagnostic_$(date -u +%Y%m%d_%H%M%S)"
mkdir -p "$OUT"
# Static route scan (very simple regex)
python3 - <<'PY' "$ROOT" "$OUT"
import sys, os, re, json, pathlib
root, out = sys.argv[1], pathlib.Path(sys.argv[2])
pat = re.compile(r'@app\.(get|post|put|delete|patch)\(\s*["\']([^"\']+)["\']')
routes=[]
for b,_,fs in os.walk(root):
    for f in fs:
        if f.endswith(".py"):
            p=os.path.join(b,f)
            try: s=open(p,"r",encoding="utf-8",errors="ignore").read()
            except: continue
            for m in pat.finditer(s):
                routes.append({"file":p,"method":m.group(1).upper(),"path":m.group(2)})
(out/"routes_static.json").write_text(json.dumps({"routes":routes},indent=2),encoding="utf-8")
PY
echo "# Diagnostic Summary" > "$OUT/SUMMARY.md"
echo "- routes_static.json" >> "$OUT/SUMMARY.md"
echo "$OUT"
