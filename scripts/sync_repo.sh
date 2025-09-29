#!/bin/zsh
set -euo pipefail

# Simple repo sync: stages changes, creates a timestamped commit, and pushes
# Usage:
#   ./scripts/sync_repo.sh                # push current branch
#   GIT_BRANCH=main ./scripts/sync_repo.sh  # force branch

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

BRANCH="${GIT_BRANCH:-}"
if [[ -z "${BRANCH}" ]]; then
  BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")
fi

echo "Syncing repo at: $REPO_ROOT (branch: $BRANCH)"

git init -b "$BRANCH" >/dev/null 2>&1 || true

git add -A

CHANGES=$(git status --porcelain)
if [[ -z "$CHANGES" ]]; then
  echo "No changes to commit."
else
  TS="$(date +%Y-%m-%dT%H:%M:%S%z)"
  git commit -m "sync: auto-save at $TS" || true
fi

git push -u origin "$BRANCH"

echo "Done."
