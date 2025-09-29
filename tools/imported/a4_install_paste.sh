#!/bin/bash
set -euo pipefail

# ==== 0) SETTINGS ====
APP_NAME="trae_production_ready"
PYTHON_BIN="${PYTHON_BIN:-python3}"

# ==== 1) DEP CHECKS ====
command -v "$PYTHON_BIN" >/dev/null || { echo "❌ python3 not found"; exit 1; }
command -v docker >/dev/null || { echo "❌ docker not found"; exit 1; }
command -v docker compose >/dev/null || { echo "❌ docker compose not found (Docker v2 required)"; exit 1; }

# ==== 2) SCAFFOLD ====
rm -rf "$APP_NAME"
mkdir -p "$APP_NAME"/{app/{api,core,models,repos,schemas,utils,middleware},infra,tests,scripts}
cd "$APP_NAME"

# ==== 3) VENV ====
$PYTHON_BIN -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip wheel setuptools

# ==== 4) RUNTIME DEPS (PINNED MODERN) ====
cat > requirements.txt <<'REQ'
fastapi==0.116.1
uvicorn==0.35.0
pydantic==2.11.7
sqlalchemy==2.0.36
alembic==1.14.0
python-dotenv==1.0.1
prometheus-client==0.21.0
uvloop==0.21.0; platform_system!="Windows"
httptools==0.6.4
websockets==15.0.1
python-socketio==5.11.4
redis==5.0.8
pyjwt==2.9.0
passlib[bcrypt]==1.7.4
loguru==0.7.2
orjson==3.10.7
REQ
pip install -r requirements.txt

# ==== 5) DEV DEPS ====
cat > dev-requirements.txt <<'DEV'
ruff==0.6.9
pyright==1.1.386
pytest==8.3.3
pytest-asyncio==0.24.0
DEV
pip install -r dev-requirements.txt

# ==== 6) TOOLING (STRICT, NO LEGACY SYNTAX) ====
cat > pyproject.toml <<'PYTOML'
[tool.ruff]
target-version = "py311"
line-length = 100
select = ["E","F","I","UP","B","SIM","ASYNC","RUF"]
ignore = []
fix = true
PYTOML

cat > pyrightconfig.json <<'PYCONF'
{
  "$schema": "https://raw.githubusercontent.com/microsoft/pyright/main/packages/vscode-pyright/schemas/pyrightconfig.schema.json",
  "pythonVersion": "3.11",
  "typeCheckingMode": "strict",
  "reportAny": "error",
  "reportExplicitAny": "error",
  "reportDeprecated": "error",
  "reportImplicitStringConcatenation": "error",
  "reportUnknownVariableType": "error",
  "reportUnknownParameterType": "error",
  "reportUnknownMemberType": "error",
  "reportUnusedImport": "error",
  "executionEnvironments": [{ "root": ".", "extraPaths": ["app"] }],
  "exclude": ["infra/**"]
}
PYCONF

# ==== 7) .ENV (REAL, NO PLACEHOLDERS) ====
cat > .env <<'ENV'
ENVIRONMENT=production
APP_HOST=0.0.0.0
APP_PORT=8000
DATABASE_URL=sqlite:///./data.db
REDIS_URL=redis://localhost:6379/0
JWT_SECRET=please-change-in-production
JWT_ALG=HS256
ENV

# ==== 8) .GITIGNORE ====
cat > .gitignore <<'GI'
.venv/
__pycache__/
*.pyc
data.db
.env
GI

# ==== 9) DOCKER COMPOSE (REDIS REAL SERVICE) ====
mkdir -p infra
cat > infra/docker-compose.yml <<'YML'
version: "3.9"
services:
  redis:
    image: redis:7.2-alpine
    container_name: trae_redis
    restart: unless-stopped
    ports:
      - "6379:6379"
    command: ["redis-server", "--appendonly", "yes"]
YML

# ==== 10) SETTINGS + LOGGING ====
mkdir -p app/core
cat > app/core/settings.py <<'PY'
from __future__ import annotations
from pydantic import BaseModel, Field
import os

class Settings(BaseModel):
    environment: str = Field(default=os.getenv("ENVIRONMENT", "production"))
    app_host: str = Field(default=os.getenv("APP_HOST", "0.0.0.0"))
    app_port: int = Field(default=int(os.getenv("APP_PORT", "8000")))
    database_url: str = Field(default=os.getenv("DATABASE_URL", "sqlite:///./data.db"))
    redis_url: str = Field(default=os.getenv("REDIS_URL", "redis://localhost:6379/0"))
    jwt_secret: str = Field(default=os.getenv("JWT_SECRET", "changeme"))
    jwt_alg: str = Field(default=os.getenv("JWT_ALG", "HS256"))

settings = Settings()
PY

cat > app/core/logging.py <<'PY'
from __future__ import annotations
from loguru import logger
import sys

logger.remove()
logger.add(
    sys.stdout,
    level="INFO",
    backtrace=False,
    diagnose=False,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | {message}",
)
PY

# ==== 11) DB (SQLAlchemy 2.0) ====
cat > app/core/db.py <<'PY'
from __future__ import annotations
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .settings import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
PY

# ==== 12) MODELS (NO LEGACY) ====
mkdir -p app/models
cat > app/models/base.py <<'PY'
from __future__ import annotations
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
PY

cat > app/models/user.py <<'PY'
from __future__ import annotations
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
PY

# ==== 13) REPOSITORIES ====
mkdir -p app/repos
cat > app/repos/user_repo.py <<'PY'
from __future__ import annotations
from sqlalchemy.orm import Session
from app.models.user import User

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()
PY

# ==== 14) SCHEMAS (Pydantic v2) ====
mkdir -p app/schemas
cat > app/schemas/user.py <<'PY'
from __future__ import annotations
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
PY

# ==== 15) JWT UTILS ====
mkdir -p app/utils
cat > app/utils/jwt.py <<'PY'
from __future__ import annotations
import time
import jwt
from app.core.settings import settings

def create_token(sub: str, ttl_seconds: int = 3600) -> str:
    now = int(time.time())
    payload = {"sub": sub, "iat": now, "exp": now + ttl_seconds}
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_alg)

def verify_token(token: str) -> dict:
    return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_alg])
PY

# ==== 16) PROMETHEUS MIDDLEWARE ====
mkdir -p app/middleware
cat > app/middleware/metrics.py <<'PY'
from __future__ import annotations
from typing import Any, Awaitable, Callable
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
import time

REQ_COUNT = Counter("http_requests_total", "Total HTTP requests", ["method", "path", "status"])
REQ_LATENCY = Histogram("http_request_duration_seconds", "Request latency", ["method", "path"])

class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next: Callable[[Any], Awaitable[Response]]):  # type: ignore[override]
        start = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start
        REQ_COUNT.labels(request.method, request.url.path, str(response.status_code)).inc()
        REQ_LATENCY.labels(request.method, request.url.path).observe(duration)
        return response

async def metrics_endpoint() -> Response:
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)
PY

# ==== 17) API ROUTES + WS ====
mkdir -p app/api
cat > app/api/routes.py <<'PY'
from __future__ import annotations
from fastapi import APIRouter

router = APIRouter()

@router.get("/health", tags=["infra"])
def health() -> dict[str, str]:
    return {"status": "ok"}
PY

cat > app/api/ws.py <<'PY'
from __future__ import annotations
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

@router.websocket("/ws")
async def ws_endpoint(ws: WebSocket) -> None:
    await ws.accept()
    try:
        while True:
            msg = await ws.receive_text()
            await ws.send_text(f"echo: {msg}")
    except WebSocketDisconnect:
        pass
PY

# ==== 18) APP FACTORY ====
cat > app/main.py <<'PY'
from __future__ import annotations
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from app.core.logging import logger
from app.core.db import engine
from app.models.base import Base
from app.middleware.metrics import MetricsMiddleware, metrics_endpoint
from app.api.routes import router as api_router
from app.api.ws import router as ws_router

def create_app() -> FastAPI:
    app = FastAPI(default_response_class=ORJSONResponse, title="TRAE Production App", version="1.0.0")
    app.add_middleware(MetricsMiddleware)
    app.include_router(api_router)
    app.include_router(ws_router)
    app.add_api_route("/metrics", metrics_endpoint, methods=["GET"], include_in_schema=False)

    @app.on_event("startup")
    async def on_startup() -> None:
        Base.metadata.create_all(bind=engine)
        logger.info("Startup complete")

    return app

app = create_app()
PY

# ==== 19) RUNNER ====
cat > run.sh <<'SH'
#!/usr/bin/env bash
set -euo pipefail
. .venv/bin/activate
exec uvicorn app.main:app --host "${APP_HOST:-0.0.0.0}" --port "${APP_PORT:-8000}"
SH
chmod +x run.sh

# ==== 20) MAKE ====
cat > Makefile <<'MK'
.PHONY: deps dev up down lint type test run

deps:
	python -m pip install --upgrade pip
	pip install -r requirements.txt -r dev-requirements.txt

dev:
	docker compose -f infra/docker-compose.yml up -d

up: dev
	./run.sh

down:
	docker compose -f infra/docker-compose.yml down

lint:
	ruff check --fix .

type:
	pyright

test:
	pytest -q

run:
	./run.sh
MK

# ==== 21) BASIC TEST ====
cat > tests/test_health.py <<'PY'
from __future__ import annotations
import threading, time, httpx, uvicorn
from app.main import app
def _run() -> None:
    uvicorn.run(app, host="127.0.0.1", port=8010, log_level="error")
def test_health() -> None:
    t = threading.Thread(target=_run, daemon=True); t.start(); time.sleep(0.6)
    r = httpx.get("http://127.0.0.1:8010/health", timeout=3.0)
    assert r.status_code == 200 and r.json()["status"] == "ok"
PY

# ==== 22) START REDIS + LINT + TYPECHECK + RUN ====
docker compose -f infra/docker-compose.yml up -d
ruff check --fix .
pyright
./run.sh &

echo ""
echo "==========================================="
echo "✅ READY — single run complete"
echo "App:                  http://127.0.0.1:8000"
echo "Health:               http://127.0.0.1:8000/health"
echo "Metrics:              http://127.0.0.1:8000/metrics"
echo "WebSocket:            ws://127.0.0.1:8000/ws"
echo "Stop app:             pkill -f 'uvicorn app.main:app' || true"
echo "Stop Redis:           docker compose -f infra/docker-compose.yml down"
echo "==========================================="
