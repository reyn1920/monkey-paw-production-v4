# Legacy MMCV Environment Setup

If you require mmcv/mmdet/mmengine stacks, use a side environment:
- Python 3.10 or 3.11 (PyTorch + OpenMMLab are not yet compatible with 3.13 on macOS ARM)
- Keep your main TraeAI venv on 3.13 for everything else

## Setup Commands

```bash
# Install pyenv if not already installed
brew install pyenv

# Install Python 3.10
pyenv install 3.10.14 -s

# Create side environment
python3 -m venv "$PROJECT_DIR/venv-py310"
source "$PROJECT_DIR/venv-py310/bin/activate"

# Install compatible versions
python -m pip install --upgrade pip setuptools wheel
pip install "torch==2.4.0" --index-url https://download.pytorch.org/whl/cpu
pip install mmengine==0.10.3 mmcv==2.1.0 mmdet==3.3.0

deactivate
```

## Usage

Only activate this environment when you need OpenMMLab functionality:

```bash
source "$PROJECT_DIR/venv-py310/bin/activate"
# Run your mmcv/mmdet code here
deactivate
```
