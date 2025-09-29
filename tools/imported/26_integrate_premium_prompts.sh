#!/bin/bash

# 🚀 Premium AI Prompts Integration Script
# Integrates system prompts from the ai-tools collection with our setup

echo "🎯 Integrating Premium AI System Prompts..."

# Set paths
PROMPTS_DIR="$HOME/Downloads/system-prompts-and-models-of-ai-tools-main"
AI_PACK_DIR="$HOME/Downloads/ultimate_vscode_ai_pack"
CURSOR_CONFIG_DIR="$HOME/Library/Application Support/Cursor/User"

# Create prompts directory in our AI pack
mkdir -p "$AI_PACK_DIR/premium_prompts"

echo "📁 Copying premium prompts..."

# Copy Cursor prompts
if [ -d "$PROMPTS_DIR/Cursor Prompts" ]; then
    cp -r "$PROMPTS_DIR/Cursor Prompts" "$AI_PACK_DIR/premium_prompts/"
    echo "✅ Cursor prompts copied"
fi

# Copy VSCode Agent prompts
if [ -d "$PROMPTS_DIR/VSCode Agent" ]; then
    cp -r "$PROMPTS_DIR/VSCode Agent" "$AI_PACK_DIR/premium_prompts/"
    echo "✅ VSCode Agent prompts copied"
fi

# Copy Cline prompts
if [ -d "$PROMPTS_DIR/Open Source prompts/Cline" ]; then
    cp -r "$PROMPTS_DIR/Open Source prompts/Cline" "$AI_PACK_DIR/premium_prompts/"
    echo "✅ Cline prompts copied"
fi

# Copy other relevant prompts
for tool in "Windsurf" "Trae" "CodeBuddy Prompts" "Manus Agent Tools & Prompt"; do
    if [ -d "$PROMPTS_DIR/$tool" ]; then
        cp -r "$PROMPTS_DIR/$tool" "$AI_PACK_DIR/premium_prompts/"
        echo "✅ $tool prompts copied"
    fi
done

echo "📋 Creating prompt integration guide..."

# Create integration guide
cat > "$AI_PACK_DIR/premium_prompts/INTEGRATION_GUIDE.md" << 'EOF'
# 🎯 Premium AI Prompts Integration Guide

## 📁 Available Prompt Collections

### 🔥 **Cursor Prompts**
- **Agent Prompt v1.2.txt** - Latest Cursor agent system prompt
- **Agent CLI Prompt** - Command-line optimized prompts
- **Chat Prompt.txt** - Enhanced chat interactions
- **Memory Prompt.txt** - Context memory management
- **Agent Tools v1.0.json** - Tool configurations

### 🤖 **VSCode Agent Prompts**
- **claude-sonnet-4.txt** - Claude Sonnet 4 optimizations
- **gpt-4.1.txt** - GPT-4.1 specific prompts
- **gpt-5.txt** - Latest GPT-5 system prompts
- **gemini-2.5-pro.txt** - Gemini Pro optimizations
- **Prompt.txt** - Base VSCode agent prompt

### 🛠️ **Cline Agent**
- **Prompt.txt** - Advanced autonomous coding prompts

### 🌪️ **Windsurf/Codeium**
- Enhanced coding assistant prompts

## 🚀 How to Use These Prompts

### **Method 1: Cursor Rules (.cursorrules)**
1. Copy content from relevant prompt files
2. Create/edit `.cursorrules` in your project root
3. Paste the prompt content

### **Method 2: AI Tool Settings**
1. Open AI tool settings (Cline, Roo Code, etc.)
2. Find "System Prompt" or "Custom Instructions"
3. Paste the appropriate prompt

### **Method 3: Chat Context**
1. Start a new chat session
2. Begin with the system prompt
3. Use for that specific conversation

## 🎯 Recommended Prompts by Use Case

### **General Coding (Cursor/Continue)**
- Use: `Cursor Prompts/Agent Prompt v1.2.txt`
- Benefits: Latest optimizations, better context handling

### **Autonomous Coding (Cline/Roo Code)**
- Use: `Open Source prompts/Cline/Prompt.txt`
- Benefits: Enhanced autonomous decision making

### **Code Review & Analysis**
- Use: `VSCode Agent/claude-sonnet-4.txt`
- Benefits: Advanced code analysis capabilities

### **Project Planning**
- Use: `Cursor Prompts/Chat Prompt.txt`
- Benefits: Better project breakdown and planning

## ⚡ Quick Setup Commands

```bash
# Copy latest Cursor prompt to project
cp "premium_prompts/Cursor Prompts/Agent Prompt v1.2.txt" .cursorrules

# Setup Cline with premium prompt
# (Paste content from Cline/Prompt.txt into Cline settings)
```

## 💡 Pro Tips

1. **Layer Prompts**: Use different prompts for different AI tools
2. **Context Matters**: Adjust prompts based on your project type
3. **Iterate**: Test different prompts to find what works best
4. **Combine**: Mix and match sections from different prompts

## 🔄 Regular Updates

- Check the original repository for prompt updates
- Re-run this integration script to get latest versions
- Subscribe to Discord for early access to new prompts

---

**These prompts represent cutting-edge AI optimization from top developers worldwide! 🌟**
EOF

echo "🎨 Creating quick-setup script..."

# Create quick setup script
cat > "$AI_PACK_DIR/scripts/apply_cursor_prompt.sh" << 'EOF'
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
EOF

chmod +x "$AI_PACK_DIR/scripts/apply_cursor_prompt.sh"

echo "📊 Creating prompt summary..."

# Show what we copied
echo ""
echo "📋 PREMIUM PROMPTS INTEGRATION SUMMARY"
echo "======================================"
find "$AI_PACK_DIR/premium_prompts" -name "*.txt" -o -name "*.json" | while read file; do
    size=$(du -h "$file" | cut -f1)
    echo "📄 $size - $(basename "$file")"
done

echo ""
echo "🎯 QUICK START:"
echo "1. cd to your project directory"
echo "2. Run: $AI_PACK_DIR/scripts/apply_cursor_prompt.sh"
echo "3. Restart Cursor to activate premium prompts"
echo ""
echo "📖 Full guide: $AI_PACK_DIR/premium_prompts/INTEGRATION_GUIDE.md"
echo ""
echo "✅ Premium AI prompts integration complete!"
