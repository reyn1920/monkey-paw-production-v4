#!/usr/bin/env bash
set -euo pipefail
if ! command -v node >/dev/null 2>&1; then
  echo "Node is required. Install via Homebrew: brew install node"
  exit 1
fi
echo "Node ready."
