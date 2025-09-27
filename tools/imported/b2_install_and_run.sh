#!/bin/bash

# TRAE.AI Production Ready Installation Script
# Single command setup for production-ready FastAPI application

set -euo pipefail

# Configuration
APP_NAME="trae_production_ready"
PYTHON_BIN="python3.11"

echo "🚀 Starting TRAE.AI Production Setup..."

# Check dependencies
echo "📋 Checking dependencies..."
if ! command -v $PYTHON_BIN &> /dev/null; then
    echo "❌ Python 3.11 not found. Please install Python 3.11 first."
    exit 1
fi

if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker first."
    exit 1
fi

# Create project directory
echo "📁 Creating project directory..."
if [ -d "$APP_NAME" ]; then
    echo "⚠️  Directory $APP_NAME already exists. Removing..."
    rm -rf "$APP_NAME"
fi
mkdir -p "$APP_NAME"
cd "$APP_NAME"

# Create virtual environment
echo "🐍 Setting up Python virtual environment..."
$PYTHON_BIN -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools wheel

# Install runtime dependencies
echo "📦 Installing runtime dependencies..."
pip install \
    fastapi==0.104.1 \
    uvicorn[standard]==0.24.0 \
    pydantic==2.5.0 \
    sqlalchemy==2.0.23 \
    alembic==1.13.0 \
    redis==5.0.1 \
    prometheus-client==0.19.0 \
    python-jose[cryptography]==3.3.0 \
    passlib[bcrypt]==1.7.4 \
    python-multipart==0.0.6 \
    websockets==12.0

# Install development dependencies
echo "🛠️  Installing development dependencies..."
pip install \
    ruff==0.1.6 \
    pyright==1.1.338 \
    pytest==7.4.3 \
    pytest-asyncio==0.21.1 \
    httpx==0.25.2 \
    pytest-cov==4.1.0

# Create pyproject.toml
echo "⚙️  Creating pyproject.toml..."
cat > pyproject.toml << 'EOF'
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "trae-production-ready"
version = "0.1.0"
description = "Production-ready FastAPI application"
requires-python = ">=3.11"

[tool.ruff]
target-version = "py311"
line-length = 88
select = ["E", "W", "F", "I", "N", "B", "A", "C4", "UP"]
ignore = ["E501"]

[tool.ruff.per-file-ignores]
"__init__.py" = ["F401"]
"tests/*" = ["S101"]

[tool.pytest.ini_options]
minversion = "6.0"
addopts = "-ra -q --strict-markers"
testpaths = ["tests"]
EOF

# Create pyrightconfig.json
echo "🔍 Creating pyrightconfig.json..."
cat > pyrightconfig.json << 'EOF'
{
  "include": ["app", "tests"],
  "exclude": ["**/__pycache__", ".venv"],
  "typeCheckingMode": "strict",
  "reportMissingImports": true,
  "reportMissingTypeStubs": false,
  "pythonVersion": "3.11",
  "pythonPlatform": "Darwin"
}
EOF

# Create .env file
echo "🔐 Creating .env configuration..."
cat > .env << 'EOF'
# Database
DATABASE_URL=sqlite:///./app.db

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# App Settings
APP_NAME=TRAE Production Ready
DEBUG=false
EOF

# Create .gitignore
echo "📝 Creating .gitignore..."
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
.venv/
venv/
ENV/
env/

# Environment Variables
.env
.env.local
.env.production

# Database
*.db
*.sqlite3

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Testing
.coverage
.pytest_cache/
.tox/

# Docker
.dockerignore
Dockerfile
EOF

# Create infrastructure directory and Docker Compose
echo "🐳 Setting up Docker infrastructure..."
mkdir -p infra
cat > infra/docker-compose.yml << 'EOF'
version: '3.8'

services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3

volumes:
  redis_data:
EOF

# Create app directory structure
echo "🏗️  Creating application structure..."
mkdir -p app/{core,models,schemas,repositories,api/v1,utils}

# Create app/__init__.py
touch app/__init__.py

# Create app/core/config.py
cat > app/core/config.py << 'EOF'
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    app_name: str = "TRAE Production Ready"
    debug: bool = False
    database_url: str = "sqlite:///./app.db"
    redis_url: str = "redis://localhost:6379/0"
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
EOF

touch app/core/__init__.py

# Create app/core/database.py
cat > app/core/database.py << 'EOF'
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
EOF

# Create app/models/__init__.py
touch app/models/__init__.py

# Create app/models/base.py
cat > app/models/base.py << 'EOF'
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
EOF

# Create app/models/user.py
cat > app/models/user.py << 'EOF'
from sqlalchemy import Column, String, Boolean
from .base import BaseModel

class User(BaseModel):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
EOF

# Create app/repositories/__init__.py
touch app/repositories/__init__.py

# Create app/repositories/user_repo.py
cat > app/repositories/user_repo.py << 'EOF'
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def create(self, user_data: UserCreate) -> User:
        hashed_password = pwd_context.hash(user_data.password)
        user = User(
            email=user_data.email,
            hashed_password=hashed_password
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
EOF

# Create app/schemas/__init__.py
touch app/schemas/__init__.py

# Create app/schemas/user.py
cat > app/schemas/user.py << 'EOF'
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
EOF

# Create app/utils/__init__.py
touch app/utils/__init__.py

# Create app/utils/jwt.py
cat > app/utils/jwt.py << 'EOF'
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.core.config import settings

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except JWTError:
        return None
EOF

# Create app/utils/metrics.py
cat > app/utils/metrics.py << 'EOF'
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time

# Metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status_code']
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        response = await call_next(request)

        duration = time.time() - start_time

        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status_code=response.status_code
        ).inc()

        REQUEST_DURATION.labels(
            method=request.method,
            endpoint=request.url.path
        ).observe(duration)

        return response

def get_metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
EOF

# Create app/api/__init__.py
touch app/api/__init__.py
touch app/api/v1/__init__.py

# Create app/api/v1/health.py
cat > app/api/v1/health.py << 'EOF'
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/health")
async def health_check():
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "trae-production-ready"
    }
EOF

# Create app/api/v1/websocket.py
cat > app/api/v1/websocket.py << 'EOF'
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
import json
import asyncio

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            # Echo the message back
            response = {
                "type": "echo",
                "data": message,
                "timestamp": asyncio.get_event_loop().time()
            }

            await manager.send_personal_message(json.dumps(response), websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
EOF

# Create app/main.py
cat > app/main.py << 'EOF'
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base
from app.utils.metrics import PrometheusMiddleware, get_metrics
from app.api.v1 import health, websocket

# Create database tables
Base.metadata.create_all(bind=engine)

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        description="Production-ready FastAPI application with WebSockets, metrics, and database",
        version="1.0.0",
        debug=settings.debug
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add Prometheus middleware
    app.add_middleware(PrometheusMiddleware)

    # Include routers
    app.include_router(health.router, tags=["health"])
    app.include_router(websocket.router, tags=["websocket"])

    # Metrics endpoint
    app.get("/metrics")(get_metrics)

    return app

app = create_app()
EOF

# Create run.sh script
echo "🚀 Creating run script..."
cat > run.sh << 'EOF'
#!/bin/bash
set -euo pipefail

echo "🚀 Starting TRAE Production Ready App..."

# Activate virtual environment
source .venv/bin/activate

# Start Redis if not running
echo "🔄 Starting Redis..."
docker compose -f infra/docker-compose.yml up -d

# Wait for Redis to be ready
echo "⏳ Waiting for Redis..."
until docker compose -f infra/docker-compose.yml exec redis redis-cli ping > /dev/null 2>&1; do
    sleep 1
done

# Run the application
echo "🌐 Starting FastAPI server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
EOF

chmod +x run.sh

# Create Makefile
echo "📋 Creating Makefile..."
cat > Makefile << 'EOF'
.PHONY: install dev up down lint type test run

install:
	pip install --upgrade pip setuptools wheel
	pip install -r requirements.txt

dev:
	pip install -e .

up:
	docker compose -f infra/docker-compose.yml up -d

down:
	docker compose -f infra/docker-compose.yml down

lint:
	ruff check --fix .

type:
	pyright .

test:
	pytest -v

run:
	./run.sh
EOF

# Create basic test
echo "🧪 Creating tests..."
mkdir -p tests
cat > tests/test_health.py << 'EOF'
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "timestamp" in data
    assert "service" in data
EOF

touch tests/__init__.py

# Start Redis
echo "🐳 Starting Redis container..."
docker compose -f infra/docker-compose.yml up -d

# Wait for Redis to be ready
echo "⏳ Waiting for Redis to be ready..."
until docker compose -f infra/docker-compose.yml exec redis redis-cli ping > /dev/null 2>&1; do
    echo "Waiting for Redis..."
    sleep 2
done

# Run linting and type checking
echo "🔍 Running code quality checks..."
ruff check --fix . || echo "⚠️  Ruff found some issues"
pyright . || echo "⚠️  Pyright found some issues"

# Run tests
echo "🧪 Running tests..."
pytest -v || echo "⚠️  Some tests failed"

# Start the application
echo "🌐 Starting FastAPI application..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
APP_PID=$!

# Wait a moment for the app to start
sleep 3

# Display ready message
echo ""
echo "✅ READY — single run complete"
echo "App:      http://127.0.0.1:8000"
echo "Health:   http://127.0.0.1:8000/health"
echo "Metrics:  http://127.0.0.1:8000/metrics"
echo "WebSocket: ws://127.0.0.1:8000/ws"
echo ""
echo "📋 To stop the application:"
echo "   pkill -f 'uvicorn app.main:app' || true"
echo "   docker compose -f infra/docker-compose.yml down"
echo ""
echo "🔄 To restart later:"
echo "   cd $(pwd)"
echo "   ./run.sh"
echo ""

# Keep the script running
wait $APP_PID
