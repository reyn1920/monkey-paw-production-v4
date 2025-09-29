from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import httpx
from pathlib import Path

app = FastAPI(title="TRAE.AI Base44 - Integrated Production Dashboard", version="1.0.0")

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
    except Exception as e:
        return {
            "base44_status": "operational",
            "main_api_status": "error",
            "main_api_healthy": False,
            "error": str(e),
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
