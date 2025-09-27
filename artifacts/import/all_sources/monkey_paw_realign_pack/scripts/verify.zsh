#!/bin/zsh
set -euo pipefail

MONKEY="${HOME}/Desktop/monkey-paw"
ADDON="${HOME}/Desktop/nocode-coder-stack"

echo "== Quick Checks =="

[[ -d "${MONKEY}" ]] || { echo "RED: core folder missing: ${MONKEY}"; exit 1; }
[[ -d "${ADDON}" ]] && echo "GREEN: addon folder present: ${ADDON}" || echo "YELLOW: addon folder not found yet (run the separator)."

if [[ -f "${MONKEY}/config/features.yaml" ]]; then
  if grep -q "nocode_stack_enabled: false" "${MONKEY}/config/features.yaml"; then
    echo "GREEN: features.yaml disables addon as intended."
  else
    echo "YELLOW: features.yaml exists but addon toggle is not set to false."
  fi
else
  echo "YELLOW: features.yaml missing."
fi

echo "Tip: Start API and hit http://127.0.0.1:8000/api/health when ready."
