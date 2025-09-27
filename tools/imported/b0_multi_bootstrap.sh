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

AUTO=0
ROOT="."

if [[ "${1:-}" == "--auto" ]]; then
  AUTO=1
  ROOT="${2:-.}"
fi

ENTRIES=()

if [[ "$AUTO" -eq 1 ]]; then
  mapfile -t ENTRIES < <(bash "$SCRIPT_DIR/auto_discover_sites.sh" "$ROOT")
else
  for entry in "${SITES[@]}"; do
    ENTRIES+=("$entry")
  done
fi

if [[ "${#ENTRIES[@]}" -eq 0 ]]; then
  echo "No site entries found."
  exit 1
fi

for entry in "${ENTRIES[@]}"; do
  IFS="::" read -r RAW_PATH RAW_REPO <<< "$entry"
  SITE_PATH="$(echo "$RAW_PATH" | xargs)"
  REPO_NAME="$(echo "$RAW_REPO" | xargs)"

  echo "-----"
  echo "Processing: path='$SITE_PATH' repo='$REPO_NAME'"
  bash "$SCRIPT_DIR/repo_init_and_push.sh" "$SITE_PATH" "$REPO_NAME"
done
