#!/usr/bin/env bash
echo 'Installing Ollama models for AI development...'

# Check if Ollama is running
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama not found. Please install Ollama first."
    exit 1
fi

echo "✅ Ollama detected!"

# Pull essential models for coding
echo "📥 Downloading coding models..."
ollama pull codellama:7b
ollama pull llama3.2:3b
ollama pull qwen2.5-coder:7b
ollama pull deepseek-coder:6.7b

# Pull general purpose models
echo "📥 Downloading general purpose models..."
ollama pull llama3.2:1b
ollama pull phi3:3.8b

echo "✅ All Ollama models installed successfully!"
echo "🎯 Available models for local AI development:"
ollama list
