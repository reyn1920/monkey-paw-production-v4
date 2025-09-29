#!/bin/bash

# Quick script to apply premium Cursor prompt to current project

PROMPTS_DIR="$HOME/Downloads/ultimate_vscode_ai_pack/premium_prompts"

echo "🎯 Applying Premium Cursor Prompt to Current Project..."

# Check if we're in a project directory
if [ ! -d ".git" ] && [ ! -f "package.json" ] && [ ! -f "requirements.txt" ] && [ ! -f "Cargo.toml" ]; then
    echo "⚠️  Warning: This doesn't look like a project directory"
    echo "🔍 Looking for: .git, package.json, requirements.txt, or Cargo.toml"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Copy the latest Cursor prompt
if [ -f "$PROMPTS_DIR/Cursor Prompts/Agent Prompt v1.2.txt" ]; then
    cp "$PROMPTS_DIR/Cursor Prompts/Agent Prompt v1.2.txt" .cursorrules
    echo "✅ Premium Cursor prompt applied to .cursorrules"
    echo "🚀 Restart Cursor to activate the new prompt"
else
    echo "❌ Cursor prompt not found. Run integrate_premium_prompts.sh first"
fi
