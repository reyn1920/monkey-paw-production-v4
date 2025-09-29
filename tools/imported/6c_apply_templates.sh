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

TARGET="${1:-}"
if [[ -z "$TARGET" ]]; then
  echo "Usage: bash scripts/apply_templates.sh <path-to-site>"
  exit 1
fi

ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
mkdir -p "$TARGET/.github/workflows" "$TARGET/.github/ISSUE_TEMPLATE"

cp -n "$ROOT/templates/.gitignore" "$TARGET/.gitignore" || true
cp -n "$ROOT/templates/.gitattributes" "$TARGET/.gitattributes" || true
cp -n "$ROOT/templates/.editorconfig" "$TARGET/.editorconfig" || true
cp -n "$ROOT/.github/workflows/checks.yml" "$TARGET/.github/workflows/checks.yml" || true
cp -n "$ROOT/ISSUE_TEMPLATE/bug_report.md" "$TARGET/.github/ISSUE_TEMPLATE/bug_report.md" || true
cp -n "$ROOT/PULL_REQUEST_TEMPLATE.md" "$TARGET/PULL_REQUEST_TEMPLATE.md" || true
cp -n "$ROOT/SECURITY.md" "$TARGET/SECURITY.md" || true
cp -n "$ROOT/CONTRIBUTING.md" "$TARGET/CONTRIBUTING.md" || true
cp -n "$ROOT/LICENSE" "$TARGET/LICENSE" || true

echo "Templates applied to $TARGET"
