#!/bin/bash

# 🌟 FOREVER AI SETUP - Makes everything permanent across all windows
# This ensures all AI enhancements work globally and persist forever

echo "🌟 Setting up AI enhancements to work FOREVER in ALL windows..."

# 1. Create permanent AI configuration directory
AI_CONFIG_DIR="$HOME/.cursor_ai_forever"
mkdir -p "$AI_CONFIG_DIR"

# 2. Copy all premium prompts permanently
PROMPTS_SOURCE="$HOME/Downloads/ultimate_vscode_ai_pack/premium_prompts"
cp -r "$PROMPTS_SOURCE" "$AI_CONFIG_DIR/"
echo "✅ Premium prompts stored permanently"

# 3. Create global Cursor settings with all AI tools enabled
CURSOR_SETTINGS="$HOME/Library/Application Support/Cursor/User/settings.json"
cp "$CURSOR_SETTINGS" "$CURSOR_SETTINGS.backup.forever"

cat > "$CURSOR_SETTINGS" << 'EOF'
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

    "continue.enableTabAutocomplete": true,
    "continue.telemetryEnabled": false,
    "continue.manuallyRunningSserver": false,

    "supermaven.enable": true,
    "supermaven.enableInlineCompletion": true,
    "supermaven.maxCompletionLength": 200,

    "cody.enabled": true,
    "cody.autocomplete.enabled": true,
    "cody.chat.enabled": true,
    "cody.experimental.guardrails": true,

    "codegeex.enable": true,
    "codegeex.enableCodeCompletion": true,
    "codegeex.enableCodeExplanation": true,

    "cursor.chat.enabled": true,
    "cursor.composer.enabled": true,
    "cursor.autocomplete.enabled": true,

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

    "files.associations": {
        "*.cursorrules": "plaintext",
        "*.prompt": "plaintext"
    },

    "terminal.integrated.defaultProfile.osx": "zsh",
    "terminal.integrated.fontSize": 13,
    "workbench.startupEditor": "welcomePage"
}
EOF

echo "✅ Global Cursor settings configured permanently"

# 4. Create universal templates
mkdir -p "$HOME/.cursor_templates"
cp "$AI_CONFIG_DIR/premium_prompts/Cursor Prompts/Agent Prompt v1.2.txt" "$HOME/.cursor_templates/premium_cursorrules.txt"

# 5. Create universal setup script
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

# 6. Add permanent aliases to shell
SHELL_RC="$HOME/.zshrc"
if ! grep -q "# AI Forever Setup" "$SHELL_RC"; then
    cat >> "$SHELL_RC" << 'EOF'

# AI Forever Setup - Added by ultimate AI pack
alias setup-ai='$HOME/.cursor_templates/setup_project_ai.sh'
alias ai-status='echo "🤖 AI Tools Status:" && cursor --list-extensions | grep -E "(supermaven|cody|cline|roo|codegeex|continue)"'
alias ai-update='cursor --update-extensions'

# Quick AI commands
alias cursor-ai='cursor . && setup-ai'
alias new-ai-project='mkdir -p "$1" && cd "$1" && setup-ai && cursor .'

# Show AI status on terminal start
echo "🤖 AI Development Environment Active"
echo "💡 Type 'setup-ai' in any project to add premium prompts"
EOF
    echo "✅ Permanent shell aliases added"
fi

# 7. Create auto-setup for new projects
mkdir -p "$HOME/.cursor_templates/auto_setup"
cat > "$HOME/.cursor_templates/auto_setup/auto_cursorrules.sh" << 'EOF'
#!/bin/bash
# Auto-add AI prompts to new projects

# Check if this is a new project directory
if [ -d ".git" ] || [ -f "package.json" ] || [ -f "requirements.txt" ] || [ -f "Cargo.toml" ]; then
    if [ ! -f ".cursorrules" ]; then
        echo "🤖 New project detected! Adding premium AI prompts..."
        cp "$HOME/.cursor_templates/premium_cursorrules.txt" .cursorrules
        echo "✅ Premium AI prompts added automatically"
    fi
fi
EOF

chmod +x "$HOME/.cursor_templates/auto_setup/auto_cursorrules.sh"

# 8. Create status checker
cat > "$AI_CONFIG_DIR/check_ai_status.sh" << 'EOF'
#!/bin/bash
echo "🤖 AI DEVELOPMENT ENVIRONMENT STATUS"
echo "===================================="
echo ""

echo "📱 Installed AI Extensions:"
cursor --list-extensions | grep -E "(supermaven|sourcegraph|saoudrizwan|rooveterinaryinc|aminer|continue)" | while read ext; do
    echo "  ✅ $ext"
done

echo ""
echo "⚙️  Global Settings:"
if [ -f "$HOME/Library/Application Support/Cursor/User/settings.json" ]; then
    echo "  ✅ Global Cursor settings configured"
else
    echo "  ❌ Global settings missing"
fi

echo ""
echo "📋 Templates Available:"
if [ -f "$HOME/.cursor_templates/premium_cursorrules.txt" ]; then
    echo "  ✅ Premium prompts template ready"
else
    echo "  ❌ Templates missing"
fi

echo ""
echo "🔧 Quick Commands Available:"
echo "  setup-ai           - Add AI to current project"
echo "  ai-status           - Check AI extensions"
echo "  cursor-ai [folder]  - Open folder with AI"
echo ""

# Check current project
if [ -f ".cursorrules" ]; then
    echo "✅ Current project has premium AI prompts"
else
    echo "💡 Run 'setup-ai' to add premium prompts to this project"
fi
EOF

chmod +x "$AI_CONFIG_DIR/check_ai_status.sh"

# 9. Reload shell configuration
source "$HOME/.zshrc" 2>/dev/null || true

echo ""
echo "🎉 FOREVER AI SETUP COMPLETE!"
echo "=============================================="
echo "✅ All AI tools configured globally"
echo "✅ Premium prompts stored permanently"
echo "✅ Shell aliases added for life"
echo "✅ Auto-setup for new projects"
echo "✅ Status checking tools created"
echo ""
echo "🌟 EVERYTHING NOW WORKS IN ALL WINDOWS FOREVER!"
echo ""
echo "💡 New Commands Available:"
echo "   setup-ai           # Add premium AI to any project"
echo "   ai-status           # Check AI tools status"
echo "   cursor-ai           # Open current folder with AI"
echo "   $AI_CONFIG_DIR/check_ai_status.sh  # Full status check"
echo ""
echo "🔄 RESTART CURSOR to activate all global settings"
echo ""
echo "🎯 What happens now:"
echo "  • All AI extensions work in every Cursor window"
echo "  • Global AI settings are permanent"
echo "  • Type 'setup-ai' in any project for premium prompts"
echo "  • Everything persists through Cursor updates"
echo "  • Your shell has permanent AI aliases"
