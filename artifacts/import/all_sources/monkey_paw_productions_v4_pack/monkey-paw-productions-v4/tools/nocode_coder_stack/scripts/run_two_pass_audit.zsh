#!/bin/zsh
set -e
ROOT="${1:-.}"
TMP1=$(mktemp); TMP2=$(mktemp)
zsh "$(dirname "$0")/run_audit_once.zsh" "$ROOT" | tee "$TMP1"
zsh "$(dirname "$0")/run_audit_once.zsh" "$ROOT" | tee "$TMP2"
if grep -qiE "(error|E[0-9]{3})" "$TMP1" || grep -qiE "(error|E[0-9]{3})" "$TMP2"; then
  echo "RED: Two-pass audit not clean"; exit 1
else
  echo "GREEN: Two-pass audit clean (heuristic)"
fi
