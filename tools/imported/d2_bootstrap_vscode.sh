#!/usr/bin/env bash
echo 'Bootstrapping Ultimate VS Code AI Pack...'

# Install essential AI extensions
echo "Installing AI extensions..."
code --install-extension GitHub.copilot
code --install-extension GitHub.copilot-chat
code --install-extension ms-python.python
code --install-extension ms-python.pylint
code --install-extension ms-python.black-formatter
code --install-extension ms-toolsai.jupyter
code --install-extension Continue.continue
code --install-extension TabNine.tabnine-vscode
code --install-extension ms-vscode.vscode-ai-toolkit
code --install-extension llm-vscode.llm-vscode

# Install additional productivity extensions
echo "Installing productivity extensions..."
code --install-extension ms-vscode.vscode-json
code --install-extension bradlc.vscode-tailwindcss
code --install-extension esbenp.prettier-vscode
code --install-extension ms-vscode.vscode-typescript-next
code --install-extension ms-vscode-remote.remote-ssh
code --install-extension ms-vscode.remote-explorer

echo "✅ VS Code AI extensions installed successfully!"
echo "🚀 You're ready for AI-powered development!"
