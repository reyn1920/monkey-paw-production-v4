#!/usr/bin/env bash
echo '🔧 Configuring VS Code for optimal AI development...'

# Create VS Code settings directory if it doesn't exist
VSCODE_SETTINGS_DIR="$HOME/Library/Application Support/Code/User"
mkdir -p "$VSCODE_SETTINGS_DIR"

# Backup existing settings
if [ -f "$VSCODE_SETTINGS_DIR/settings.json" ]; then
    echo "📋 Backing up existing settings..."
    cp "$VSCODE_SETTINGS_DIR/settings.json" "$VSCODE_SETTINGS_DIR/settings.json.backup"
fi

# Apply AI-optimized settings
echo "⚙️ Applying AI-optimized settings..."
cp vscode_ai_settings.json "$VSCODE_SETTINGS_DIR/settings.json"

echo "✅ VS Code configured for AI development!"
echo "💡 Tip: Restart VS Code to apply all changes"
