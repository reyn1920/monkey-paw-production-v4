# 🚀 Next-Stage Production Tuning Checklist
**MacBook Air M1 (16GB) → Production-Ready Performance**

After completing your baseline FastAPI performance testing, use this checklist to push toward production-level optimization.

## 📊 Current Baseline Results
- ✅ FastAPI `/api/status`: 797 req/s, 1.59ms avg latency
- ✅ Paste app `/paste/`: 613 req/s
- ✅ Root endpoint `/`: 821 req/s
- ⚠️ Target: 2k-5k req/s for simple endpoints

---

## 🎯 Stage 1: Worker & Process Optimization

### [ ] 1.1 Upgrade to Gunicorn + Uvicorn Workers
```bash
# Install production WSGI server
pip install gunicorn

# Start with optimized workers
python start_fastapi_optimized.py --gunicorn
```
**Expected improvement:** 30-50% throughput increase

### [ ] 1.2 Fine-tune Worker Count
```bash
# Test different worker configurations
# Rule: (2 × CPU cores) + 1 for I/O bound apps
# M1 has 8 cores → try 3-5 workers

# Test 3 workers
gunicorn app.main:app -w 3 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000

# Test 4 workers
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```
**Target:** Find sweet spot between throughput and memory usage

### [ ] 1.3 Enable Worker Recycling
```bash
# Prevent memory leaks with worker recycling
gunicorn app.main:app \
  -w 4 \
  -k uvicorn.workers.UvicornWorker \
  --max-requests 1000 \
  --max-requests-jitter 100 \
  --preload-app
```
**Benefit:** Stable memory usage, prevents worker bloat

---

## 🗄️ Stage 2: Database & Connection Pooling

### [ ] 2.1 Implement Database Connection Pooling
```python
# For PostgreSQL with asyncpg
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,          # Base connections
    max_overflow=30,       # Additional connections
    pool_pre_ping=True,    # Validate connections
    pool_recycle=3600,     # Recycle after 1 hour
)
```
**Expected improvement:** 2-3x database query performance

### [ ] 2.2 Add Redis Caching Layer
```bash
# Install Redis
brew install redis
redis-server

# Add to requirements.txt
redis>=4.0.0
aioredis>=2.0.0
```
```python
# Cache frequently accessed data
import aioredis

@lru_cache(maxsize=1000)
async def get_cached_data(key: str):
    # Implementation with Redis
    pass
```
**Target:** <10ms response time for cached endpoints

### [ ] 2.3 Optimize Database Queries
- [ ] Add database indexes for frequent queries
- [ ] Use `select_related()`/`prefetch_related()` for ORM
- [ ] Implement query result pagination
- [ ] Add database query monitoring

---

## 🌐 Stage 3: Advanced Nginx Configuration

### [ ] 3.1 Enable HTTP/2 and Compression
```nginx
#/etc/nginx/sites-available/your-app
server {
    listen 443 ssl http2;

    # Compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css application/json application/javascript;

    # Brotli (better compression)
    brotli on;
    brotli_comp_level 6;
    brotli_types text/plain text/css application/json application/javascript;
}
```
**Expected improvement:** 20-40% faster asset delivery

### [ ] 3.2 Optimize Nginx Worker Configuration
```nginx
#/etc/nginx/nginx.conf
worker_processes auto;  # Use all CPU cores
worker_connections 2048;  # Increase from 1024

events {
    use epoll;  # Linux optimization
    multi_accept on;
}

http {
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    keepalive_requests 1000;
}
```

### [ ] 3.3 Add Rate Limiting & Security
```nginx
# Rate limiting
limit_req_zone $binary_remote_addr zone=api:10m rate=100r/m;
limit_req_zone $binary_remote_addr zone=general:10m rate=300r/m;

server {
    # Apply rate limits
    location/api/{
        limit_req zone=api burst=20 nodelay;
        proxy_pass http://fastapi_backend;
    }

    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
}
```

---

## 📈 Stage 4: Monitoring & Observability

### [ ] 4.1 Add Application Performance Monitoring
```python
# Install APM tools
pip install prometheus-client
pip install structlog

# Add metrics endpoint
from prometheus_client import Counter, Histogram, generate_latest

REQUEST_COUNT = Counter('requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('request_duration_seconds', 'Request duration')

@app.middleware("http")
async def metrics_middleware(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time

    REQUEST_COUNT.labels(request.method, request.url.path).inc()
    REQUEST_DURATION.observe(duration)

    return response
```

### [ ] 4.2 Set Up Health Checks
```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": "1.0.0",
        "database": await check_database_health(),
        "redis": await check_redis_health()
    }
```

### [ ] 4.3 Add Structured Logging
```python
import structlog

logger = structlog.get_logger()

@app.middleware("http")
async def logging_middleware(request, call_next):
    start_time = time.time()

    response = await call_next(request)

    logger.info(
        "request_completed",
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        duration=time.time() - start_time
    )

    return response
```

---

## 🔧 Stage 5: Advanced Optimizations

### [ ] 5.1 Implement Response Caching
```python
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

# Initialize cache
FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

@app.get("/api/data")
@cache(expire=300)  # Cache for 5 minutes
async def get_data():
    # Expensive operation
    return await fetch_data_from_db()
```

### [ ] 5.2 Add Background Task Processing
```python
from celery import Celery

# For CPU-intensive tasks
celery_app = Celery('tasks', broker='redis://localhost:6379')

@celery_app.task
def process_heavy_computation(data):
    # Move heavy work to background
    return result

@app.post("/api/process")
async def trigger_processing(data: dict):
    task = process_heavy_computation.delay(data)
    return {"task_id": task.id, "status": "processing"}
```

### [ ] 5.3 Optimize Static Asset Delivery
```nginx
# Nginx static file optimization
location/static/{
    alias/path/to/static/files/;
    expires 1y;
    add_header Cache-Control "public, immutable";

    # Enable compression for static files
    gzip_static on;
    brotli_static on;
}

# CDN integration (optional)
location/assets/{
    proxy_pass https://your-cdn.com/assets/;
    proxy_cache_valid 200 1d;
}
```

---

## 📊 Stage 6: Load Testing & Validation

### [ ] 6.1 Comprehensive Load Testing
```bash
# Install advanced load testing tools
brew install wrk
pip install locust

# Test with wrk (more realistic than hey)
wrk -t12 -c400 -d30s --latency http://localhost:8000/api/status

# Test with Locust (Python-based, more flexible)
locust -f load_test.py --host=http://localhost:8000
```

### [ ] 6.2 Create Load Test Scenarios
```python
# load_test.py
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def view_status(self):
        self.client.get("/api/status")

    @task(2)
    def view_paste(self):
        self.client.get("/paste/")

    @task(1)
    def create_paste(self):
        self.client.post("/paste/", json={
            "content": "test content",
            "language": "python"
        })
```

### [ ] 6.3 Performance Benchmarking
```bash
# Run comprehensive benchmark
python fastapi_performance_baseline.py

# Target metrics after optimization:
# - Simple endpoints: 5k-10k req/s
# - Database queries: 2k-5k req/s
# - p95 latency: <25ms
# - p99 latency: <100ms
# - Memory usage: <4GB total
```

---

## 🎯 Production Readiness Targets

### Performance Targets (MacBook Air M1)
- [ ] **Throughput:** 5k+ req/s for simple endpoints
- [ ] **Latency:** p95 < 25ms, p99 < 100ms
- [ ] **Memory:** <4GB total usage
- [ ] **CPU:** <70% utilization under load
- [ ] **Error Rate:** <0.1% under normal load

### Reliability Targets
- [ ] **Uptime:** 99.9% availability
- [ ] **Recovery:** <30s restart time
- [ ] **Monitoring:** Full observability stack
- [ ] **Alerts:** Automated incident detection

### Security Targets
- [ ] **Rate Limiting:** API protection enabled
- [ ] **Headers:** Security headers configured
- [ ] **SSL/TLS:** HTTPS with proper certificates
- [ ] **Secrets:** No hardcoded credentials

---

## 🚀 Deployment Pipeline (Next Phase)

Once you've optimized performance locally, the next step is setting up a production deployment pipeline:

1. **Containerization:** Docker multi-stage builds
2. **Orchestration:** Kubernetes or Docker Swarm
3. **CI/CD:** GitHub Actions → staging → production
4. **Infrastructure:** Cloud deployment (AWS/GCP/Azure)
5. **Monitoring:** Production observability stack

---

## 📝 Quick Start Commands

```bash
# 1. Start optimized FastAPI
python start_fastapi_optimized.py --gunicorn

# 2. Run performance baseline
python fastapi_performance_baseline.py

# 3. Load test with wrk
wrk -t8 -c200 -d30s --latency http://localhost:8000/api/status

# 4. Monitor system resources
htop  # Watch CPU/memory usage
```

---

**💡 Pro Tip:** Work through these stages incrementally. Test performance after each optimization to measure the impact. The M1 MacBook Air can easily handle 10k+ req/s with proper tuning!

**🎯 Goal:** Transform your 797 req/s baseline into a 5k+ req/s production-ready application.
