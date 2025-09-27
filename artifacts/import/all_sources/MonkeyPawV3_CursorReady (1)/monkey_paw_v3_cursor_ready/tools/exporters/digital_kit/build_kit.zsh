#!/bin/zsh
set -e
mkdir -p artifacts/published
zip -r artifacts/published/digital_kit.zip artifacts/staging >/dev/null
echo "Wrote artifacts/published/digital_kit.zip"
