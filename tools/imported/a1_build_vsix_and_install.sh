#!/usr/bin/env bash
set -e
if ! command -v npx >/dev/null 2>&1; then echo "npx not found"; exit 2; fi
if ! command -v code >/dev/null 2>&1; then echo "VS Code CLI 'code' not found"; exit 2; fi
cd vsc-ollama-assistant
npx @vscode/vsce package -o ../vsc-ollama-assistant-0.0.4.vsix
cd ..
code --install-extension ./vsc-ollama-assistant-0.0.4.vsix
echo "[VSIX] Installed. Reload VS Code if needed."
