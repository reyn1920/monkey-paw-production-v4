#!/usr/bin/env zsh
set -euo pipefail

PYBIN="$(command -v python3 || true)"
PIPBIN="$(command -v pip3 || true)"
if [[ -z "$PYBIN" ]]; then
  echo "Python3 not found."; exit 1
fi

need_pkg(){ python3 - <<'PY'
import importlib, sys
mods = sys.argv[1:]
for m in mods:
    try: importlib.import_module(m)
    except Exception: print(m)
PY
}

MISSING=($(need_pkg fastapi uvicorn yaml pydantic))
if (( ${#MISSING[@]} > 0 )); then
  if command -v pipx >/dev/null 2>&1; then
    pipx ensurepath || true
  fi
  for pkg in fastapi "uvicorn[standard]" pyyaml "pydantic<3":
    if [[ "$pkg" == "pydantic<3" ]]; then
      $PIPBIN install 'pydantic<3' --quiet || true
    else
      $PIPBIN install "$pkg" --quiet || true
    fi
  done
fi

cd "$(dirname "$0")/.."
python3 -c 'import sys; from app.main import app; print("App import OK")' >/dev/null
exec uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
