#!/usr/bin/env bash
echo "=== Diagnostics ==="
echo "[OS]" && sw_vers || true
echo "[Node]" && node -v 2>/dev/null || echo "node not found"
echo "[VS Code]" && code -v 2>/dev/null || echo "code CLI not found"
echo "[Ollama]" && ollama --version 2>/dev/null || echo "ollama not found"
echo "[Chrome]" && /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version 2>/dev/null || echo "chrome app not found"
echo "[Keybindings path]" && echo "$HOME/Library/Application Support/Code/User/keybindings.json"
echo "==================="
