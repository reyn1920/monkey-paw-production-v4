#!/usr/bin/env bash
set -e
echo "[Install] Installing local extension without VSIX..."
SRC="vsc-ollama-assistant"
NAME="local.vsc-ollama-assistant-0.0.4"
DEST="$HOME/.vscode/extensions/$NAME"
rm -rf "$DEST"
mkdir -p "$DEST"
cp -R "$SRC"/* "$DEST"/
echo "[Install] Installed to $DEST"
echo "[Install] Reload VS Code (Cmd+Shift+P → Developer: Reload Window)"
