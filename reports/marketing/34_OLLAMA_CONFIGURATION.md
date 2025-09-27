# Ollama Configuration Guide

This guide provides comprehensive documentation for configuring Ollama integration in your application.

## Overview

Ollama is a local AI model runner that allows you to run large language models on your own hardware. This integration provides a cost-effective alternative to cloud-based AI services while maintaining privacy and control over your data.

## Environment Variables

### Core Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `USE_OLLAMA` | `1` | Enable/disable Ollama integration (1=enabled, 0=disabled) |
| `OLLAMA_ENDPOINT` | `http://localhost:11434` | Ollama service endpoint URL |
| `OLLAMA_URL` | `http://127.0.0.1:11434` | Alternative endpoint configuration |
| `OLLAMA_MODEL` | `llama3` | Default model to use for generation |

### Generation Parameters

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_TEMPERATURE` | `0.8` | Controls randomness (0.0-2.0, lower = more focused) |
| `OLLAMA_MAX_TOKENS` | `800` | Maximum tokens to generate |
| `OLLAMA_TOP_P` | `0.9` | Nucleus sampling parameter (0.0-1.0) |
| `OLLAMA_TOP_K` | `40` | Top-K sampling parameter |
| `OLLAMA_REPEAT_PENALTY` | `1.1` | Penalty for repetition (1.0 = no penalty) |
| `OLLAMA_CONTEXT_LENGTH` | `4096` | Maximum context window size |

### Service Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_TIMEOUT` | `30` | General timeout in seconds |
| `OLLAMA_CONNECT_TIMEOUT` | `10` | Connection timeout in seconds |
| `OLLAMA_READ_TIMEOUT` | `60` | Read timeout in seconds |
| `OLLAMA_HOST` | `localhost` | Ollama service host |
| `OLLAMA_PORT` | `11434` | Ollama service port |

### Logging and Debugging

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_DEBUG` | `false` | Enable debug logging |
| `OLLAMA_VERBOSE` | `false` | Enable verbose logging |

## Model Categories

### General Purpose Models

**Recommended for**: General text generation, conversation, content creation

- `llama3.1:8b` - Latest Llama 3.1 8B (balanced performance)
- `llama3.1:70b` - Latest Llama 3.1 70B (high performance)
- `llama3:8b` - Llama 3 8B (stable version)
- `mistral:7b` - Mistral 7B (efficient general purpose)
- `mixtral:8x7b` - Mixtral 8x7B (mixture of experts)

### Code-Specialized Models

**Recommended for**: Code generation, debugging, technical documentation

- `codellama:7b` - Code Llama 7B (code generation)
- `codellama:13b` - Code Llama 13B (better code understanding)
- `deepseek-coder:6.7b` - DeepSeek Coder (specialized coding)
- `wizardcoder:15b` - WizardCoder (code generation)
- `starcoder:15b` - StarCoder (code completion)

### Lightweight Models

**Recommended for**: Resource-constrained environments, fast responses

- `phi3:3.8b` - Microsoft Phi-3 (ultra efficient)
- `qwen2:0.5b` - Qwen2 0.5B (minimal resource usage)
- `tinyllama:1.1b` - TinyLlama (extremely lightweight)
- `gemma:2b` - Google Gemma 2B (ultra lightweight)

### Specialized Models

**Recommended for**: Specific use cases like vision, chat optimization

- `llava:7b` - LLaVA (vision and language)
- `neural-chat:7b` - Neural Chat (conversation optimized)
- `vicuna:7b` - Vicuna (chat optimized)

## Configuration Examples

### Development Environment (.env.local)

```bash
# Enable Ollama for development
USE_OLLAMA=1
OLLAMA_MODEL=codellama:13b
OLLAMA_TEMPERATURE=0.7
OLLAMA_DEBUG=true
OLLAMA_VERBOSE=true
```

### Production Environment

```bash
# Production Ollama configuration
USE_OLLAMA=1
OLLAMA_MODEL=llama3.1:8b
OLLAMA_TEMPERATURE=0.8
OLLAMA_MAX_TOKENS=1000
OLLAMA_TIMEOUT=45
OLLAMA_DEBUG=false
OLLAMA_VERBOSE=false
```

### Lightweight Setup

```bash
# Minimal resource configuration
USE_OLLAMA=1
OLLAMA_MODEL=phi3:3.8b
OLLAMA_MAX_TOKENS=500
OLLAMA_CONTEXT_LENGTH=2048
OLLAMA_TEMPERATURE=0.9
```

## Installation and Setup

### 1. Install Ollama

```bash
# macOS
curl -fsSL https://ollama.ai/install.sh | sh

# Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows
# Download from https://ollama.ai/download
```

### 2. Start Ollama Service

```bash
ollama serve
```

### 3. Pull Required Models

```bash
# Pull a general purpose model
ollama pull llama3.1:8b

# Pull a coding model
ollama pull codellama:13b

# Pull a lightweight model
ollama pull phi3:3.8b
```

### 4. Verify Installation

```bash
# Check available models
ollama list

# Test model
ollama run llama3.1:8b "Hello, how are you?"
```

## Performance Tuning

### Model Selection Guidelines

| Use Case | Recommended Model | RAM Required | Performance |
|----------|------------------|--------------|-------------|
| Development | `codellama:13b` | 8GB+ | High coding accuracy |
| Production | `llama3.1:8b` | 6GB+ | Balanced performance |
| Lightweight | `phi3:3.8b` | 4GB+ | Fast responses |
| Coding | `deepseek-coder:6.7b` | 6GB+ | Specialized coding |
| Chat | `neural-chat:7b` | 6GB+ | Conversation optimized |

### Parameter Tuning

- **Temperature**: Lower (0.1-0.3) for factual/coding tasks, higher (0.7-1.0) for creative tasks
- **Top-P**: 0.9 is generally good, lower for more focused responses
- **Max Tokens**: Adjust based on expected response length
- **Context Length**: Larger for complex tasks, smaller for performance

## Troubleshooting

### Common Issues

1. **Connection Refused**
   - Ensure Ollama service is running: `ollama serve`
   - Check port availability: `lsof -i :11434`

2. **Model Not Found**
   - Pull the model: `ollama pull <model-name>`
   - Check available models: `ollama list`

3. **Out of Memory**
   - Use a smaller model (e.g., `phi3:3.8b`)
   - Reduce context length
   - Close other applications

4. **Slow Responses**
   - Use GPU acceleration if available
   - Reduce max_tokens
   - Use a smaller model

### Debug Mode

Enable debug logging to troubleshoot issues:

```bash
export OLLAMA_DEBUG=true
export OLLAMA_VERBOSE=true
```

## Security Considerations

- Ollama runs locally, keeping your data private
- No API keys or external credentials required
- Models and conversations stay on your machine
- Consider firewall rules if exposing Ollama externally

## Integration with Application

The application automatically detects Ollama configuration through environment variables. The adapter handles:

- Automatic fallback when Ollama is unavailable
- Health checks and service monitoring
- Parameter validation and error handling
- Logging and debugging support

## Best Practices

1. **Model Management**: Keep only necessary models to save disk space
2. **Resource Monitoring**: Monitor RAM and CPU usage during model execution
3. **Fallback Strategy**: Always have fallback responses when Ollama is unavailable
4. **Testing**: Test with different models to find optimal performance
5. **Updates**: Regularly update Ollama and models for improvements

## Support and Resources

- [Ollama Official Documentation](https://ollama.ai/docs)
- [Model Library](https://ollama.ai/library)
- [GitHub Repository](https://github.com/ollama/ollama)
- [Community Discord](https://discord.gg/ollama)