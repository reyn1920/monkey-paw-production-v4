# Creative Studio Setup Guide

This guide provides comprehensive setup instructions for building a local creative studio on Apple Silicon, integrating Ollama, ComfyUI, Linly Talker, and cloud software tools based on extensive research and optimization findings.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Core Components Setup](#core-components-setup)
3. [Apple Silicon Optimization](#apple-silicon-optimization)
4. [Cloud Software Integration](#cloud-software-integration)
5. [Workflow Configuration](#workflow-configuration)
6. [Performance Tuning](#performance-tuning)
7. [Troubleshooting](#troubleshooting)

## System Requirements

### Hardware Requirements
- **Apple Silicon Mac** (M1, M2, M3, or M4 series)
- **Minimum RAM**: 16GB (32GB+ recommended for optimal performance)
- **Storage**: 100GB+ free space for models and cache
- **macOS**: 12.0+ (Monterey or later)

### Performance Expectations by Hardware

| Hardware | RAM | Expected Performance | Recommended Models |
|----------|-----|---------------------|--------------------|
| M1 8GB | 8GB | Basic workflows | llama3.2:3b, gemma2:2b |
| M1 16GB+ | 16GB+ | Full workflows | llama3.2:7b, codellama:7b |
| M2/M3 16GB+ | 16GB+ | Advanced workflows | llama3.2:8b, llava:7b |
| M4 32GB+ | 32GB+ | Professional workflows | llama3.2:70b (quantized) |

## Core Components Setup

### 1. Ollama LLM Engine Setup

#### Installation
```bash
# Method 1: Homebrew (Recommended)
brew install ollama

# Method 2: Direct download
curl -fsSL https://ollama.com/install.sh | sh
```

#### Service Management
```bash
# Start Ollama service
brew services start ollama

# Or run manually
ollama serve
```

#### Model Installation
```bash
# Essential models for creative studio
ollama pull llama3.2:3b      # Primary lightweight model
ollama pull gemma2:2b         # Fallback model
ollama pull llava:7b          # Vision model for image understanding
ollama pull codellama:7b      # Code generation

# Optional advanced models (requires more RAM)
ollama pull llama3.2:8b       # Better quality, more RAM
ollama pull mistral:7b        # Alternative high-quality model
```

#### Performance Optimization
```bash
# Set environment variables for Apple Silicon
export OLLAMA_HOST=0.0.0.0:11434
export OLLAMA_ORIGINS="*"
export OLLAMA_NUM_PARALLEL=1
export OLLAMA_MAX_LOADED_MODELS=2
```

#### Verification
```bash
# Test Ollama installation
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2:3b",
  "prompt": "Hello, world!",
  "stream": false
}'
```

### 2. ComfyUI Visual Engine Setup

#### Prerequisites
```bash
# Install Python 3.10+ (if not already installed)
brew install python@3.10

# Create virtual environment
python3 -m venv comfyui_env
source comfyui_env/bin/activate
```

#### Installation
```bash
# Clone ComfyUI repository
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI

# Install dependencies with Apple Silicon optimization
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt

# Install additional dependencies for Apple Silicon
pip install accelerate transformers diffusers
```

#### Apple Silicon Configuration
```bash
# Create launch script for Apple Silicon
cat > launch_comfyui_m1.sh << 'EOF'
#!/bin/bash
export PYTORCH_ENABLE_MPS_FALLBACK=1
export PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0

python main.py --force-fp16 --use-split-cross-attention --use-pytorch-cross-attention
EOF

chmod +x launch_comfyui_m1.sh
```

#### Model Setup
```bash
# Create models directory structure
mkdir -p models/checkpoints
mkdir -p models/vae
mkdir -p models/loras
mkdir -p models/controlnet

# Download essential models (examples)
# Note: You'll need to download these from HuggingFace or other sources
# wget -O models/checkpoints/sd_xl_base_1.0.safetensors [MODEL_URL]
```

#### Launch ComfyUI
```bash
# Start ComfyUI with Apple Silicon optimization
./launch_comfyui_m1.sh

# Or use the standard launch
python main.py --listen 0.0.0.0 --port 8188
```

#### Verification
```bash
# Test ComfyUI API
curl http://localhost:8188/system_stats
```

### 3. Linly Talker AI Avatar Setup

#### Installation
```bash
# Clone Linly Talker repository
git clone https://github.com/Kedreamix/Linly-Talker.git
cd Linly-Talker

# Create virtual environment
python3 -m venv linly_env
source linly_env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Model Download
```bash
# Download required models
bash scripts/download_models.sh

# Or download manually:
# - LLM models (Chinese-LLaMA-2-7B-hf)
# - ASR models (Whisper-large-v2)
# - TTS models (EdgeTTS)
# - Avatar models (SadTalker)
```

#### Apple Silicon Optimization
```bash
# Create optimized launch script
cat > run_m1_optimized.py << 'EOF'
import os
os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = '1'
os.environ['PYTORCH_MPS_HIGH_WATERMARK_RATIO'] = '0.0'

# Import and run main application
from demo_app import main

if __name__ == "__main__":
    main()
EOF
```

#### Launch Linly Talker
```bash
# Start the application
python run_m1_optimized.py --mode demo

# Or use the standard demo
python demo_app.py
```

## Apple Silicon Optimization

### Memory Management
```bash
# Add to your shell profile (.zshrc or .bash_profile)
export PYTORCH_ENABLE_MPS_FALLBACK=1
export PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0
export OMP_NUM_THREADS=8
export MKL_NUM_THREADS=8
```

### Performance Monitoring
```bash
# Monitor system resources
sudo powermetrics --samplers smc -n 1 | grep -E "CPU die temperature|GPU die temperature|Package Power"

# Monitor memory usage
vm_stat | head -20

# Monitor GPU usage (if available)
sudo powermetrics --samplers gpu_power -n 1
```

### Thermal Management
- Keep your Mac well-ventilated
- Consider using a laptop stand for better airflow
- Monitor temperatures during intensive operations
- Use Activity Monitor to track resource usage

## Cloud Software Integration

### 1. Lingo Blaster Integration

#### API Setup
```bash
# Set environment variables
export LINGO_BLASTER_API_KEY="your_api_key_here"
export YOUTUBE_API_KEY="your_youtube_api_key"
```

#### Features Available
- YouTube video translation (100+ languages)
- 3-click workflow integration
- Auto-ranking and SEO optimization
- Batch processing capabilities

### 2. Captionizer (Captions.ai) Integration

#### API Setup
```bash
# Set environment variables
export CAPTIONIZER_API_KEY="your_api_key_here"
```

#### Features Available
- AI-powered caption generation
- Multi-language support
- Style customization
- Real-time editing capabilities

## Workflow Configuration

### 1. Complete Media Creation Pipeline

```yaml
# Example workflow configuration
workflow:
  name: "complete_media_creation"
  steps:
    1:
      component: "ollama"
      action: "enhance_prompt"
      model: "llama3.2:3b"
    2:
      component: "comfyui"
      action: "generate_visual"
      workflow: "text_to_image"
    3:
      component: "linly_talker"
      action: "create_avatar"
      voice: "default"
    4:
      component: "captionizer"
      action: "add_captions"
      style: "modern"
    5:
      component: "lingo_blaster"
      action: "translate"
      languages: ["en", "es", "fr"]
```

### 2. AI Avatar Creation Workflow

```python
# Example Python workflow
from creative_studio_integration import CreativeStudio

studio = CreativeStudio()

# Generate script with Ollama
script = studio.ollama.generate_script("Create a 2-minute presentation about AI")

# Create avatar with Linly Talker
avatar_video = studio.linly_talker.create_avatar(
    script=script,
    voice="professional",
    avatar_style="business"
)

# Enhance with ComfyUI
enhanced_video = studio.comfyui.enhance_video(
    video=avatar_video,
    style="professional",
    background="office"
)
```

## Performance Tuning

### 1. Model Optimization

#### Ollama Model Selection
```bash
# For 8GB RAM systems
ollama pull llama3.2:3b
ollama pull gemma2:2b

# For 16GB+ RAM systems
ollama pull llama3.2:7b
ollama pull codellama:7b
ollama pull llava:7b

# For 32GB+ RAM systems
ollama pull llama3.2:8b
ollama pull mistral:7b
```

#### ComfyUI Optimization
```python
# Launch arguments for different RAM configurations

# 8GB RAM
python main.py --force-fp16 --use-split-cross-attention --lowvram

# 16GB RAM
python main.py --force-fp16 --use-split-cross-attention

# 32GB+ RAM
python main.py --force-fp16
```

### 2. Concurrent Processing

```python
# Example of optimized concurrent processing
import asyncio
from concurrent.futures import ThreadPoolExecutor

async def process_media_pipeline(input_data):
    with ThreadPoolExecutor(max_workers=3) as executor:
        # Run components in parallel where possible
        ollama_task = executor.submit(ollama_process, input_data)
        comfyui_task = executor.submit(comfyui_process, input_data)

        # Wait for results
        ollama_result = await asyncio.wrap_future(ollama_task)
        comfyui_result = await asyncio.wrap_future(comfyui_task)

        # Sequential processing for dependent tasks
        avatar_result = await linly_talker_process(ollama_result)

        return combine_results(comfyui_result, avatar_result)
```

### 3. Resource Management

```bash
# Create resource monitoring script
cat > monitor_resources.sh << 'EOF'
#!/bin/bash
while true; do
    echo "=== $(date) ==="
    echo "Memory Usage:"
    vm_stat | grep -E "Pages (free|active|inactive|speculative|wired down)"
    echo "\nCPU Usage:"
    top -l 1 | grep "CPU usage"
    echo "\nGPU Usage:"
    sudo powermetrics --samplers gpu_power -n 1 2>/dev/null | grep "GPU Power" || echo "GPU monitoring not available"
    echo "\n"
    sleep 30
done
EOF

chmod +x monitor_resources.sh
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Ollama Issues

**Problem**: Ollama service not starting
```bash
# Solution: Check and restart service
brew services stop ollama
brew services start ollama

# Check logs
tail -f $(brew --prefix)/var/log/ollama.log
```

**Problem**: Model loading errors
```bash
# Solution: Clear model cache and re-download
rm -rf ~/.ollama/models/[problematic_model]
ollama pull [model_name]
```

#### 2. ComfyUI Issues

**Problem**: Out of memory errors
```bash
# Solution: Use lower memory settings
python main.py --force-fp16 --use-split-cross-attention --lowvram --cpu
```

**Problem**: Model loading failures
```bash
# Solution: Check model file integrity
ls -la models/checkpoints/
# Re-download corrupted models
```

#### 3. Linly Talker Issues

**Problem**: Avatar generation fails
```bash
# Solution: Check model dependencies
python -c "import torch; print(torch.backends.mps.is_available())"

# Reinstall with MPS support
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio
```

#### 4. Apple Silicon Specific Issues

**Problem**: MPS backend errors
```bash
# Solution: Fallback to CPU
export PYTORCH_ENABLE_MPS_FALLBACK=1

# Or disable MPS entirely
export PYTORCH_DISABLE_MPS=1
```

**Problem**: Memory pressure warnings
```bash
# Solution: Reduce concurrent processes
# Monitor with Activity Monitor
# Close unnecessary applications
# Reduce model sizes or use quantized versions
```

### Performance Benchmarks

#### Expected Generation Times (Apple Silicon)

| Task | M1 8GB | M1 16GB | M2 16GB | M3/M4 32GB |
|------|--------|---------|---------|------------|
| Text Generation (100 tokens) | 5-10s | 3-5s | 2-4s | 1-3s |
| Image Generation (512x512) | 30-60s | 20-40s | 15-30s | 10-20s |
| Avatar Video (30s) | 5-10min | 3-5min | 2-4min | 1-3min |
| Complete Pipeline | 10-15min | 6-10min | 4-8min | 3-6min |

### Optimization Tips

1. **Model Selection**: Choose models appropriate for your RAM
2. **Batch Processing**: Process multiple items together when possible
3. **Resource Monitoring**: Keep an eye on memory and thermal throttling
4. **Sequential vs Parallel**: Balance concurrent processing with resource limits
5. **Model Caching**: Keep frequently used models loaded
6. **Storage**: Use fast SSD storage for model files and cache

### Getting Help

- **Ollama**: [GitHub Issues](https://github.com/ollama/ollama/issues)
- **ComfyUI**: [GitHub Issues](https://github.com/comfyanonymous/ComfyUI/issues)
- **Linly Talker**: [GitHub Issues](https://github.com/Kedreamix/Linly-Talker/issues)
- **Apple Silicon Optimization**: [Apple Developer Forums](https://developer.apple.com/forums/)

---

## Next Steps

1. Follow the setup instructions for each component
2. Test individual components before integration
3. Configure workflows based on your specific needs
4. Monitor performance and optimize as needed
5. Integrate cloud software APIs when available

This setup provides a comprehensive foundation for a local creative studio optimized for Apple Silicon hardware.
