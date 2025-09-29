# M1 MacBook Air Optimized FastAPI Configuration

# Uvicorn Configuration
HOST = "0.0.0.0"
PORT = 8080
WORKERS = 4  # Optimal for M1 8-core system
WORKER_CLASS = "uvicorn.workers.UvicornWorker"
MAX_REQUESTS = 1000
MAX_REQUESTS_JITTER = 100
KEEPALIVE = 2

# Memory Management
WORKER_CONNECTIONS = 1000
WORKER_TMP_DIR = "/tmp"

# M1 Specific Optimizations
USE_UVLOOP = True  # Enable uvloop for better async performance
USE_MPS = True  # Enable Metal Performance Shaders

# Environment Variables for M1
import os  # Fixed incomplete statement  # Fixed incomplete statement  # Fixed incomplete statement  # Fixed incomplete statement

os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
os.environ["OMP_NUM_THREADS"] = "8"
os.environ["MKL_NUM_THREADS"] = "8"

# Gunicorn Configuration
bind = f"{HOST}:{PORT}"
workers = WORKERS
worker_class = WORKER_CLASS
max_requests = MAX_REQUESTS
max_requests_jitter = MAX_REQUESTS_JITTER
keepalive = KEEPALIVE
worker_connections = WORKER_CONNECTIONS
worker_tmp_dir = WORKER_TMP_DIR

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = (
    '%%(h)s %%(l)s %%(u)s %%(t)s "%%(r)s" %%(s)s %%(b)s "%%(f)s" "%%(a)s" %%(D)s'
)
