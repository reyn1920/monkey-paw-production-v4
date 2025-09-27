#!/bin/bash

echo "🔍 Cursor AI Environment Verification"
echo "====================================="

# Check Ollama installation and models
echo ""
echo "🤖 Checking Ollama models..."
if command -v ollama >/dev/null 2>&1; then
    echo "✅ Ollama is installed"
    echo "📦 Available models:"
    ollama list | head -10
else
    echo "❌ Ollama not found"
fi

# Check Cursor installation
echo ""
echo "📱 Checking Cursor installation..."
if [ -d "/Applications/Cursor.app" ]; then
    echo "✅ Cursor is installed"

    # Check settings file
    CURSOR_SETTINGS="$HOME/Library/Application Support/Cursor/User/settings.json"
    if [ -f "$CURSOR_SETTINGS" ]; then
        echo "✅ Cursor settings configured"
        echo "📝 Settings location: $CURSOR_SETTINGS"
    else
        echo "⚠️  Cursor settings not found"
    fi
else
    echo "❌ Cursor not found in Applications"
fi

# Check VS Code/Cursor CLI
echo ""
echo "🔧 Checking CLI tools..."
if command -v cursor >/dev/null 2>&1; then
    echo "✅ Cursor CLI available"
elif command -v code >/dev/null 2>&1; then
    echo "✅ VS Code CLI available (compatible with Cursor)"
else
    echo "⚠️  No CLI tools found"
fi

# Check key extensions
echo ""
echo "🔌 Checking AI extensions..."
EXTENSION_DIR="$HOME/.vscode/extensions"
if [ -d "$EXTENSION_DIR" ]; then
    if ls "$EXTENSION_DIR" | grep -q "continue.continue"; then
        echo "✅ Continue extension found"
    else
        echo "⚠️  Continue extension not found"
    fi

    if ls "$EXTENSION_DIR" | grep -q "tabnine.tabnine"; then
        echo "✅ TabNine extension found"
    else
        echo "⚠️  TabNine extension not found"
    fi

    if ls "$EXTENSION_DIR" | grep -q "ms-python.python"; then
        echo "✅ Python extension found"
    else
        echo "⚠️  Python extension not found"
    fi
else
    echo "⚠️  Extensions directory not found"
fi

echo ""
echo "🎯 Setup Summary:"
echo "=================="
echo "1. Open Cursor from Applications"
echo "2. Press Cmd+L to test AI chat"
echo "3. Press Cmd+K for inline AI editing"
echo "4. Use Tab for AI autocomplete"
echo ""
echo "📚 Documentation: CURSOR_SETUP_COMPLETE.md"
echo "🚀 Happy coding with AI!"
