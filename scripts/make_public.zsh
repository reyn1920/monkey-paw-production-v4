#!/bin/zsh
set -euo pipefail
# Temporarily make repo public so web assistants can read code
# Usage: ./scripts/make_public.zsh [owner/repo]
REPO="${1:-reyn1920/monkey-paw-production-v4}"
echo "Making $REPO public..."
gh repo edit "$REPO" --visibility public
REPO_URL="https://github.com/${REPO}"
echo "Repo is PUBLIC: $REPO_URL"
