#!/bin/bash

# 🌍 Global Premium Prompts Setup
# Makes premium AI prompts work in ALL Cursor projects

echo "🌍 Setting up GLOBAL premium AI prompts..."

CURSOR_SETTINGS="$HOME/Library/Application Support/Cursor/User/settings.json"
PROMPTS_DIR="$HOME/Downloads/ultimate_vscode_ai_pack/premium_prompts"

# Backup current settings
cp "$CURSOR_SETTINGS" "$CURSOR_SETTINGS.backup.$(date +%Y%m%d_%H%M%S)"
echo "💾 Backup created: $CURSOR_SETTINGS.backup.$(date +%Y%m%d_%H%M%S)"

# Create enhanced global settings with premium prompts
cat > /tmp/cursor_global_settings.json << 'EOF'
{
    "editor.fontSize": 14,
    "editor.fontFamily": "SF Mono, Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace",
    "editor.tabSize": 2,
    "editor.insertSpaces": true,
    "editor.wordWrap": "on",
    "editor.minimap.enabled": false,
    "editor.lineNumbers": "on",
    "editor.renderWhitespace": "selection",
    "workbench.colorTheme": "Default Dark+",
    "workbench.iconTheme": "vs-seti",
    "files.autoSave": "onFocusChange",
    "files.trimTrailingWhitespace": true,
    "files.insertFinalNewline": true,

    // AI Tools Global Configuration
    "continue.enableTabAutocomplete": true,
    "continue.telemetryEnabled": false,
    "continue.manuallyRunningSserver": false,

    // Supermaven Configuration
    "supermaven.enable": true,
    "supermaven.enableInlineCompletion": true,
    "supermaven.maxCompletionLength": 200,

    // Sourcegraph Cody Configuration
    "cody.enabled": true,
    "cody.autocomplete.enabled": true,
    "cody.chat.enabled": true,
    "cody.experimental.guardrails": true,

    // CodeGeeX Configuration
    "codegeex.enable": true,
    "codegeex.enableCodeCompletion": true,
    "codegeex.enableCodeExplanation": true,

    // Global AI Assistant Settings
    "cursor.chat.enabled": true,
    "cursor.composer.enabled": true,
    "cursor.autocomplete.enabled": true,

    // Enhanced Global AI Instructions
    "cursor.general.defaultRules": [
        "You are an expert AI coding assistant with advanced reasoning capabilities.",
        "Follow best practices for clean, maintainable, and secure code.",
        "Provide detailed explanations and consider edge cases.",
        "Use modern frameworks and libraries appropriately.",
        "Always test your code suggestions thoroughly.",
        "Be proactive in suggesting improvements and optimizations.",
        "Handle errors gracefully and provide helpful debugging information.",
        "Consider performance implications of your suggestions.",
        "Follow the project's existing code style and conventions.",
        "Provide comprehensive documentation for complex code."
    ],

    // File associations and AI behavior
    "files.associations": {
        "*.cursorrules": "plaintext",
        "*.prompt": "plaintext"
    },

    // Terminal and workspace settings
    "terminal.integrated.defaultProfile.osx": "zsh",
    "terminal.integrated.fontSize": 13,
    "workbench.startupEditor": "welcomePage"
}
EOF

# Apply the global settings
cp /tmp/cursor_global_settings.json "$CURSOR_SETTINGS"
echo "✅ Global premium AI settings applied"

# Create a universal .cursorrules template
mkdir -p "$HOME/.cursor_templates"
cp "$PROMPTS_DIR/Cursor Prompts/Agent Prompt v1.2.txt" "$HOME/.cursor_templates/premium_cursorrules.txt"
echo "📋 Universal .cursorrules template created"

# Create global setup script
cat > "$HOME/.cursor_templates/setup_project_ai.sh" << 'EOF'
#!/bin/bash
# Quick script to add premium AI to any project

if [ ! -f ".cursorrules" ]; then
    cp "$HOME/.cursor_templates/premium_cursorrules.txt" .cursorrules
    echo "✅ Premium AI prompt added to project"
    echo "🚀 Restart Cursor to activate"
else
    echo "⚠️  .cursorrules already exists"
    echo "🔄 Run with --force to overwrite"
    if [ "$1" = "--force" ]; then
        cp "$HOME/.cursor_templates/premium_cursorrules.txt" .cursorrules
        echo "✅ Premium AI prompt updated"
    fi
fi
EOF

chmod +x "$HOME/.cursor_templates/setup_project_ai.sh"

# Add to shell profile for easy access
SHELL_RC="$HOME/.zshrc"
if ! grep -q "setup_project_ai" "$SHELL_RC"; then
    echo "" >> "$SHELL_RC"
    echo "# Quick AI setup for any project" >> "$SHELL_RC"
    echo "alias setup-ai='$HOME/.cursor_templates/setup_project_ai.sh'" >> "$SHELL_RC"
    echo "🔧 Added 'setup-ai' command to your shell"
fi

echo ""
echo "🎯 GLOBAL AI SETUP COMPLETE!"
echo "============================================"
echo "✅ Premium AI settings applied globally"
echo "✅ Universal template created"
echo "✅ Quick setup command added"
echo ""
echo "📋 NEW FEATURES:"
echo "1. Enhanced AI behavior in ALL Cursor windows"
echo "2. Run 'setup-ai' in any project to add premium prompts"
echo "3. All AI extensions work globally"
echo ""
echo "🚀 RESTART CURSOR to activate global settings"
echo ""
echo "💡 Quick commands:"
echo "   setup-ai           # Add premium AI to current project"
echo "   setup-ai --force   # Overwrite existing .cursorrules"
EOF
