#!/usr/bin/env zsh
set -euo pipefail
ROOT="${1:-$PWD}"
OUT="$HOME/Desktop/nocode-coder-stack"
echo "Copy‑based separation to: $OUT"
mkdir -p "$OUT"
patterns=( "nocode" "lowcode" "agent-builder" "promptbuilder" "autocoder" )
for pat in $patterns; do
  fd_cmd=$(command -v fd || command -v fdfind || true)
  if [[ -n "$fd_cmd" ]]; then
    $fd_cmd -HI "$pat" "$ROOT" | while read -r f; do
      if [[ -f "$f" ]]; then
        dest="$OUT/${f#$ROOT/}"
        mkdir -p "$(dirname "$dest")"
        cp -a "$f" "$dest" || true
      fi
    done
  else
    # portable fallback
    grep -ril "$pat" "$ROOT" | while read -r f; do
      if [[ -f "$f" ]]; then
        dest="$OUT/${f#$ROOT/}"
        mkdir -p "$(dirname "$dest")"
        cp -a "$f" "$dest" || true
      fi
    done
  fi
done
cfg="$ROOT/apps/monkey_paw_live/config/config.yaml"
if [[ -f "$cfg" ]]; then
  python3 - "$cfg" <<'PY'
import sys, yaml, pathlib
p = pathlib.Path(sys.argv[1])
data = yaml.safe_load(p.read_text(encoding="utf-8"))
data.setdefault("flags", {})["nocode_stack_enabled"] = False
p.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
print("Flag set: flags.nocode_stack_enabled=false")
PY
fi
echo "Done."
