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

SITE_PATH="$1"
REPO_NAME="$2"

if [[ ! -d "$SITE_PATH" ]]; then
  echo "Missing directory: $SITE_PATH"
  exit 1
fi

cd "$SITE_PATH"

if [[ ! -d ".git" ]]; then
  git init
  git checkout -b main
fi

git config user.email >/dev/null 2>&1 || git config user.email "noreply@users.noreply.github.com"
git config user.name  >/dev/null 2>&1 || git config user.name  "TRAE.AI"

"$SCRIPT_DIR/apply_templates.sh" "$SITE_PATH"

git add -A
git commit -m "Initial commit via TRAE.AI bootstrap" || true

API="https://api.github.com"
REPO_URL="$API/repos/$GITHUB_OWNER/$REPO_NAME"
RESP=$(curl -s -H "Authorization: token $GITHUB_TOKEN" "$REPO_URL")
if echo "$RESP" | grep -q '"message": "Not Found"'; then
  echo "Creating repo $GITHUB_OWNER/$REPO_NAME"
  curl -s -X POST "$API/user/repos" \
    -H "Authorization: token $GITHUB_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"name\":\"$REPO_NAME\",\"private\":true}" >/dev/null
else
  echo "Repo $GITHUB_OWNER/$REPO_NAME exists or is accessible."
fi

if git remote get-url origin >/dev/null 2>&1; then
  :
else
  git remote add origin "https://github.com/$GITHUB_OWNER/$REPO_NAME.git"
fi

git push -u origin main
echo "Pushed $SITE_PATH to https://github.com/$GITHUB_OWNER/$REPO_NAME"
