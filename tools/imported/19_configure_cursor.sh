#!/bin/bash

echo "🎯 Configuring Cursor AI Environment..."

# Set up Cursor settings directory
CURSOR_SETTINGS_DIR="$HOME/Library/Application Support/Cursor/User"
mkdir -p "$CURSOR_SETTINGS_DIR"

# Copy settings to Cursor
echo "📝 Applying Cursor AI settings..."
cp ../vscode_ai_settings.json "$CURSOR_SETTINGS_DIR/settings.json"

# Check if Cursor CLI is available
if command -v cursor >/dev/null 2>&1; then
    echo "� Installing Cursor extensions via CLI..."
    cursor --install-extension ms-python.python
    cursor --install-extension ms-python.black-formatter
    cursor --install-extension ms-python.pylint
    cursor --install-extension ms-jupyter.jupyter
    cursor --install-extension continue.continue
    cursor --install-extension tabnine.tabnine-vscode
    cursor --install-extension ms-vscode.vscode-typescript-next
    cursor --install-extension esbenp.prettier-vscode
    cursor --install-extension bradlc.vscode-tailwindcss
elif command -v code >/dev/null 2>&1; then
    echo "🔌 Installing extensions via VS Code CLI (compatible with Cursor)..."
    
    # Core Python Development
    code --install-extension ms-python.python
    code --install-extension ms-python.black-formatter
    code --install-extension ms-python.pylint
    code --install-extension ms-toolsai.jupyter
    
    # FREE AI Extensions (No Subscription Required)
    echo "🆓 Installing FREE AI coding assistants..."
    code --install-extension continue.continue              # Local AI with Ollama
    code --install-extension codeium.codeium               # Windsurf Plugin (FREE)
    code --install-extension supermaven.supermaven         # Fast FREE autocomplete
    code --install-extension sourcegraph.cody-ai           # FREE AI with codebase context
    code --install-extension blackboxapp.blackbox         # FREE coding copilot
    code --install-extension saoudrizwan.claude-dev       # Cline - Autonomous AI agent
    code --install-extension rooveterinaryinc.roo-cline   # Roo Code - FREE AI team
    code --install-extension aminer.codegeex              # CodeGeeX - FREE AI assistant
    
    # Development Tools
    code --install-extension ms-vscode.vscode-typescript-next
    code --install-extension esbenp.prettier-vscode
    code --install-extension bradlc.vscode-tailwindcss
else
    echo "⚠️  No CLI available. Please install extensions manually in Cursor:"
    echo ""
    echo "🆓 FREE AI Extensions (No subscription required):"
    echo "   ✅ Continue - Local AI with your Ollama models"
    echo "   ✅ Windsurf Plugin (Codeium) - FREE AI autocomplete"
    echo "   ✅ Supermaven - Fastest FREE autocomplete"
    echo "   ✅ Sourcegraph Cody - FREE AI with codebase context"
    echo "   ✅ BLACKBOX AI - FREE coding copilot"
    echo "   ✅ Cline - Autonomous AI coding agent"
    echo "   ✅ Roo Code - Complete AI dev team"
    echo "   ✅ CodeGeeX - FREE multilingual AI assistant"
    echo ""
    echo "🛠️ Development Tools:"
    echo "   - Python Extension Pack"
    echo "   - Jupyter Notebooks"
    echo "   - Prettier Code Formatter"
    echo "   - Tailwind CSS IntelliSense"
fi

# Create symlink for easier Cursor CLI access
if [ -d "/Applications/Cursor.app" ]; then
    echo "🔗 Creating Cursor CLI symlink..."
    sudo ln -sf "/Applications/Cursor.app/Contents/Resources/app/bin/cursor" /usr/local/bin/cursor 2>/dev/null || true
fi

echo "✅ Cursor AI environment configured!"
echo "🚀 Settings applied to: $CURSOR_SETTINGS_DIR/settings.json"
echo "📱 Open Cursor and enjoy your AI-powered development environment!"
echo ""
echo "🎯 Quick Start Guide:"
echo "   1. Open Cursor"
echo "   2. Press Cmd+L for AI chat"
echo "   3. Use Tab for AI autocomplete"
echo "   4. Press Cmd+K for inline AI editing"
