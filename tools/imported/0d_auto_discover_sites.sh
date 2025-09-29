#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${GITHUB_TOKEN:-}" ]]; then
  echo "GITHUB_TOKEN not set; export a token with repo scope."
  exit 1
fi

if [[ -z "${GITHUB_OWNER:-}" ]]; then
  echo "GITHUB_OWNER not set; export your GitHub username or org."
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/sites.env"

ROOT="${1:-.}"

discover_candidates() {
  # Prefer known names if present
  if [[ -d "$ROOT/online_production" ]]; then
    echo "$ROOT/online_production"
  fi
  if [[ -d "$ROOT/base44-app" ]]; then
    echo "$ROOT/base44-app"
  fi

  # Generic discovery: look for Node/Python/git signals
  find "$ROOT" -maxdepth 1 -mindepth 1 -type d | while read -r d; do
    name="$(basename "$d")"
    [[ "$name" == ".git" ]] && continue
    [[ "$name" == "scripts" ]] && continue
    [[ "$name" == "__pycache__" ]] && continue
    [[ "$name" == "venv" || "$name" == ".venv" ]] && continue

    if [[ -d "$d/.git" ]] || [[ -f "$d/package.json" ]] || [[ -f "$d/requirements.txt" ]] || [[ -f "$d/backend/app/main.py" ]]; then
      echo "$d"
    fi
  done
}

mapfile -t ALL < <(discover_candidates | awk '!seen[$0]++')
SELECTED=()
for d in "${ALL[@]}"; do
  if [[ "$d" == "$SCRIPT_DIR/.." ]]; then
    continue
  fi
  SELECTED+=("$d")
  [[ "${#SELECTED[@]}" -ge 4 ]] && break
done

if [[ "${#SELECTED[@]}" -eq 0 ]]; then
  echo "No candidate sites found under '$ROOT'."
  exit 2
fi

for d in "${SELECTED[@]}"; do
  base="$(basename "$d")"
  repo="$(echo "$base" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-')"
  echo "$d :: $repo"
done
