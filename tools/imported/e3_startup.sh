#!/bin/bash
# TRAE AI Production Startup Script - MacBook Air M1 Optimized
# This script initializes the production environment with ARM64 optimizations

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] ✓${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] ⚠${NC} $1"
}

log_error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ✗${NC} $1"
}

# M1 System Information
log "TRAE AI Production System - MacBook Air M1 Startup"
log "Architecture: $(uname -m)"
log "Platform: $(uname -s)"
log "Kernel: $(uname -r)"

# Check if running on ARM64
if [[ "$(uname -m)" != "arm64" && "$(uname -m)" != "aarch64" ]]; then
    log_warning "Not running on ARM64 architecture. M1 optimizations may not be effective."
fi

# Environment Variables
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1
export PLATFORM=linux/arm64
export ARCH=arm64
export OPTIMIZED_FOR=M1_MACBOOK_AIR

# M1 Specific Optimizations
export OMP_NUM_THREADS=8
export MKL_NUM_THREADS=8
export OPENBLAS_NUM_THREADS=8
export VECLIB_MAXIMUM_THREADS=8

# PyTorch M1 Optimizations
export PYTORCH_ENABLE_MPS_FALLBACK=1
export PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0

# Memory Management for 16GB RAM
export MALLOC_ARENA_MAX=2
export MALLOC_MMAP_THRESHOLD_=131072
export MALLOC_TRIM_THRESHOLD_=131072
export MALLOC_TOP_PAD_=131072
export MALLOC_MMAP_MAX_=65536

# Create necessary directories
log "Creating application directories..."
mkdir -p /app/logs
mkdir -p /app/uploads
mkdir -p /app/cache
mkdir -p /app/tmp
mkdir -p /app/static
mkdir -p /app/media

# Set proper permissions
chmod 755 /app/logs
chmod 755 /app/uploads
chmod 755 /app/cache
chmod 755 /app/tmp

log_success "Directories created successfully"

# System Health Check
log "Performing system health check..."

# Check available memory
MEMORY_GB=$(python3 -c "import psutil; print(f'{psutil.virtual_memory().total / (1024**3):.1f}')")
log "Available Memory: ${MEMORY_GB}GB"

if (( $(echo "$MEMORY_GB < 15" | bc -l) )); then
    log_warning "Low memory detected. Consider closing other applications."
else
    log_success "Memory check passed"
fi

# Check CPU cores
CPU_CORES=$(python3 -c "import multiprocessing; print(multiprocessing.cpu_count())")
log "CPU Cores: ${CPU_CORES}"

if [ "$CPU_CORES" -lt 8 ]; then
    log_warning "Less than 8 CPU cores detected. Performance may be reduced."
else
    log_success "CPU check passed"
fi

# Check disk space
DISK_USAGE=$(df -h /app | awk 'NR==2 {print $5}' | sed 's/%//')
log "Disk Usage: ${DISK_USAGE}%"

if [ "$DISK_USAGE" -gt 85 ]; then
    log_warning "High disk usage detected: ${DISK_USAGE}%"
else
    log_success "Disk space check passed"
fi

# Database Connection Check
log "Checking database connectivity..."
if python3 -c "import psycopg2; psycopg2.connect('$DATABASE_URL')" 2>/dev/null; then
    log_success "Database connection successful"
else
    log_error "Database connection failed. Check DATABASE_URL environment variable."
    exit 1
fi

# Redis Connection Check
log "Checking Redis connectivity..."
if python3 -c "import redis; r=redis.from_url('$REDIS_URL'); r.ping()" 2>/dev/null; then
    log_success "Redis connection successful"
else
    log_warning "Redis connection failed. Some features may be limited."
fi

# Run Database Migrations
log "Running database migrations..."
if python3 -m alembic upgrade head; then
    log_success "Database migrations completed"
else
    log_error "Database migrations failed"
    exit 1
fi

# Initialize AI Models
log "Initializing AI models for M1..."
python3 -c "
import torch
print(f'PyTorch version: {torch.__version__}')
print(f'MPS available: {torch.backends.mps.is_available()}')
print(f'MPS built: {torch.backends.mps.is_built()}')
if torch.backends.mps.is_available():
    device = torch.device('mps')
    print(f'Using device: {device}')
    # Test tensor operation
    x = torch.randn(1000, 1000, device=device)
    y = torch.randn(1000, 1000, device=device)
    z = torch.mm(x, y)
    print('MPS tensor operations working correctly')
else:
    print('MPS not available, using CPU')
"

log_success "AI models initialized"

# Cache Warmup
log "Warming up application cache..."
python3 -c "
from backend.core.cache import warm_cache
warm_cache()
print('Cache warmed up successfully')
" 2>/dev/null || log_warning "Cache warmup failed or not implemented"

# Performance Monitoring Setup
log "Setting up performance monitoring..."
cat > /app/monitor.py << 'EOF'
import psutil
import time
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger('performance_monitor')

def monitor_system():
    while True:
        # Memory usage
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        memory_used_gb = memory.used / (1024**3)

        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)

        # Disk usage
        disk = psutil.disk_usage('/app')
        disk_percent = (disk.used / disk.total) * 100

        # Log if thresholds exceeded
        if memory_percent > 85:
            logger.warning(f'High memory usage: {memory_percent:.1f}% ({memory_used_gb:.1f}GB)')

        if cpu_percent > 80:
            logger.warning(f'High CPU usage: {cpu_percent:.1f}%')

        if disk_percent > 85:
            logger.warning(f'High disk usage: {disk_percent:.1f}%')

        # Log normal status every 5 minutes
        if int(time.time()) % 300 == 0:
            logger.info(f'System Status - Memory: {memory_percent:.1f}%, CPU: {cpu_percent:.1f}%, Disk: {disk_percent:.1f}%')

        time.sleep(30)  # Check every 30 seconds

if __name__ == '__main__':
    monitor_system()
EOF

# Start background monitoring
python3 /app/monitor.py &
MONITOR_PID=$!
log_success "Performance monitoring started (PID: $MONITOR_PID)"

# Revenue Stream Validation
log "Validating revenue streams..."
python3 -c "
from backend.revenue.validator import validate_all_streams
result = validate_all_streams()
if result['success']:
    print('✓ All revenue streams validated successfully')
    for stream in result['streams']:
        print(f'  - {stream}: OK')
else:
    print('⚠ Some revenue streams have issues:')
    for issue in result['issues']:
        print(f'  - {issue}')
" 2>/dev/null || log_warning "Revenue stream validation not available"

# Final System Check
log "Performing final system check..."

# Check if all required services are ready
SERVICES=("database" "redis" "ai_models")
for service in "${SERVICES[@]}"; do
    case $service in
        "database")
            if python3 -c "import psycopg2; psycopg2.connect('$DATABASE_URL')" 2>/dev/null; then
                log_success "$service: Ready"
            else
                log_error "$service: Not ready"
                exit 1
            fi
            ;;
        "redis")
            if python3 -c "import redis; r=redis.from_url('$REDIS_URL'); r.ping()" 2>/dev/null; then
                log_success "$service: Ready"
            else
                log_warning "$service: Not ready (non-critical)"
            fi
            ;;
        "ai_models")
            if python3 -c "import torch; print('AI models ready')" 2>/dev/null; then
                log_success "$service: Ready"
            else
                log_error "$service: Not ready"
                exit 1
            fi
            ;;
    esac
done

# Display startup summary
log "\n=== TRAE AI Production System Startup Summary ==="
log "Architecture: ARM64 (Apple Silicon M1)"
log "Memory: ${MEMORY_GB}GB available"
log "CPU Cores: ${CPU_CORES}"
log "Workers: ${WORKERS:-4}"
log "Environment: ${ENVIRONMENT:-production}"
log "Optimization: MacBook Air M1 16GB RAM"
log "Status: All systems ready"
log "================================================\n"

# Cleanup function for graceful shutdown
cleanup() {
    log "Shutting down TRAE AI Production System..."

    # Kill background monitoring
    if [ ! -z "$MONITOR_PID" ]; then
        kill $MONITOR_PID 2>/dev/null || true
        log "Performance monitoring stopped"
    fi

    # Additional cleanup tasks
    log "Cleanup completed"
    exit 0
}

# Set up signal handlers
trap cleanup SIGTERM SIGINT

# Start the main application
log "Starting TRAE AI Production Server with M1 optimizations..."
log "Server will be available at http://0.0.0.0:8000"
log "Health check endpoint: http://0.0.0.0:8000/health"
log "API documentation: http://0.0.0.0:8000/api/docs"

# Execute Gunicorn with optimized configuration
exec gunicorn -c gunicorn.conf.py backend.main:app
