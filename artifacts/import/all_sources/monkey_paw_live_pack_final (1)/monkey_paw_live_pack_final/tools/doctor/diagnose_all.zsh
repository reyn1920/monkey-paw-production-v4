#!/bin/zsh
set -e
mkdir -p reports
echo "Health: $(date)" > reports/DIAGNOSIS.txt
echo "Python: $(python3 --version)" >> reports/DIAGNOSIS.txt
echo "PIP: $(python3 -m pip --version)" >> reports/DIAGNOSIS.txt
echo "FastAPI present? $(python3 - <<'PY'
try:
 import fastapi; print('yes')
except Exception:
 print('no')
PY
)" >> reports/DIAGNOSIS.txt
echo "OK" 
