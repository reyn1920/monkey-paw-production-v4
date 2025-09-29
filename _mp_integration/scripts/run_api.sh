#!/bin/bash
# Start the FastAPI backend for the integration pack
cd "$(dirname "$0")/../backend" || exit 1
uvicorn main:app --host 127.0.0.1 --port 8000
