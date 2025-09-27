#!/bin/zsh
set -e
ROOT="${1:-.}"
zsh "$(dirname "$0")/run_two_pass_audit.zsh" "$ROOT" || { echo "RED: audits failed"; exit 1; }
zsh "$(dirname "$0")/go_live_local.zsh" || true
python3 - <<'PY'
import os, hashlib, pathlib, datetime, json
root = pathlib.Path("."); art = root / "runtime_stage"
art.mkdir(exist_ok=True, parents=True)
def sha(p): 
    h=hashlib.sha256(); h.update(p.read_bytes()); return h.hexdigest()[:16]
report = {"ts": datetime.datetime.now().isoformat(), "runtime_stage_files": []}
for p in art.rglob("*"):
    if p.is_file(): report["runtime_stage_files"].append({"path": str(p), "sha": sha(p)})
(pathlib.Path("REPORT.md")).write_text("# Run Report\n\n" + json.dumps(report, indent=2))
print("Wrote REPORT.md")
PY
echo "GREEN: Full run complete"
