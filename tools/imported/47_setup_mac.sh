#!/usr/bin/env bash
set -euo pipefail
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip wheel setuptools
pip install fastapi==0.115.0 uvicorn[standard]==0.30.6 pydantic==2.9.2 starlette==0.40.0 aiosqlite==0.20.0 edge-tts==6.1.12 pillow==10.4.0
echo READY
