import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import FastAPI with proper error handling
try:
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
except ImportError:
    print(
        "FastAPI not found. Please ensure it's installed: pip install fastapi uvicorn[standard]"
    )
    sys.exit(1)

app = FastAPI()

# Health check endpoint


@app.get("/api/health")
async def health_check():
    return {"status": "green"}


# Mount routers with try/except blocks
try:
    from routers.policy_router import router as policy_router

    app.include_router(policy_router, tags=["policy"])
except ImportError as e:
    print(f"Failed to import policy_router: {e}")
except Exception as e:
    print(f"Error mounting policy_router: {e}")

# Skip comprehensive_dashboard as it uses mock classes incompatible with FastAPI
# try:
#     from routers.comprehensive_dashboard import router as dashboard_router
#     app.include_router(dashboard_router, prefix="/api/dashboard", tags=["dashboard"])
# except ImportError as e:
#     print(f"Failed to import comprehensive_dashboard: {e}")

try:
    from routers.software_status import router as software_status_router

    app.include_router(software_status_router, tags=["software"])
except ImportError as e:
    print(f"Failed to import software_status: {e}")
except Exception as e:
    print(f"Error mounting software_status: {e}")

if __name__ == "__main__":
    try:
        import uvicorn

        uvicorn.run(app, host="0.0.0.0", port=8080)
    except ImportError:
        print(
            "Uvicorn not found. Please ensure it's installed: pip install uvicorn[standard]"
        )
        sys.exit(1)
