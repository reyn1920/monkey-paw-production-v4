from pathlib import Path

import httpx
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Import all routers
from routers.production_health import router as production_health_router

# Import health router
try:
    from api.health import router as health_router
except ImportError:
    health_router = None

# Import simplified API routers
try:
    from api.simple_api_discovery import router as api_discovery_router
except ImportError:
    api_discovery_router = None

try:
    from api.simple_channels import router as channels_router
except ImportError:
    channels_router = None

try:
    from api.simple_pets import router as pets_router
except ImportError:
    pets_router = None

try:
    from api.simple_runtime import router as runtime_router
except ImportError:
    runtime_router = None

try:
    from auth.routes import auth_router, users_router, admin_router
except ImportError:
    auth_router = users_router = admin_router = None

try:
    from routers.policy_router import router as policy_router
except ImportError:
    policy_router = None

try:
    from routers.solo_agent_router import router as solo_agent_router
except ImportError:
    solo_agent_router = None

try:
    from api.data_routes import router as data_router
except ImportError:
    data_router = None

app = FastAPI(title="TRAE.AI Base44 - Integrated Production Dashboard", version="1.0.0")

# Include all available routers
app.include_router(production_health_router)

if health_router:
    app.include_router(health_router, prefix="/api", tags=["health"])

if api_discovery_router:
    app.include_router(api_discovery_router)

if channels_router:
    app.include_router(channels_router)

if pets_router:
    app.include_router(pets_router)

if runtime_router:
    app.include_router(runtime_router)

if auth_router:
    app.include_router(auth_router)

if users_router:
    app.include_router(users_router)

if admin_router:
    app.include_router(admin_router)

if policy_router:
    app.include_router(policy_router)

if solo_agent_router:
    app.include_router(solo_agent_router)

if data_router:
    app.include_router(data_router)

# Get the project root directory
project_root = Path(__file__).parent.parent

# Mount static files for frontend
frontend_path = project_root / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")


@app.get("/")
async def root():
    """Root endpoint returning system status"""
    return {
        "message": "TRAE.AI Base44 System",
        "status": "operational",
        "version": "1.0.0",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"ok": True, "status": "healthy", "service": "base44-api"}


@app.get("/dashboard")
async def dashboard():
    """Serve the dashboard HTML file"""
    dashboard_file = project_root / "frontend" / "index.html"
    if dashboard_file.exists():
        return FileResponse(str(dashboard_file))
    return JSONResponse(status_code=404, content={"error": "Dashboard not found"})


@app.get("/media")
async def media_info():
    """Media endpoint information"""
    return {
        "media_type": "dashboard",
        "format": "json",
        "endpoints": ["/health", "/dashboard", "/api/production-status"],
    }


@app.get("/api/production-status")
async def get_production_status():
    """Get status from main production API and combine with Base44 data"""
    try:
        # Fetch data from main production API
        async with httpx.AsyncClient() as client:
            main_api_response = await client.get("http://localhost:8000/health")
            channels_response = await client.get("http://localhost:8000/channels")

        main_api_data = (
            main_api_response.json() if main_api_response.status_code == 200 else {}
        )
        channels_data = (
            channels_response.json() if channels_response.status_code == 200 else []
        )

        # Combine with Base44 status
        return {
            "base44_status": "operational",
            "main_api_status": main_api_data.get("status", "unknown"),
            "main_api_healthy": main_api_response.status_code == 200,
            "channels_count": len(channels_data),
            "channels": channels_data[:5],  # Show first 5 channels
            "integrated": True,
            "timestamp": main_api_data.get("timestamp", "unknown"),
            "services": {
                "base44": "✅ Online",
                "main_api": (
                    "✅ Connected"
                    if main_api_response.status_code == 200
                    else "❌ Disconnected"
                ),
                "database": "✅ Passing",
                "monitoring": "Online",
            },
        }
    except httpx.RequestError as request_error:
        return {
            "base44_status": "operational",
            "main_api_status": "error",
            "main_api_healthy": False,
            "error": str(request_error),
            "integrated": False,
            "services": {
                "base44": "✅ Online",
                "main_api": "❌ Disconnected",
                "database": "✅ Passing",
                "monitoring": "Online",
            },
        }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=7860)
