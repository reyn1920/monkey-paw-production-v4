import uvicorn  # Fixed incomplete statement  # Fixed incomplete statement  # Fixed incomplete statement  # Fixed incomplete statement
from fastapi import (
    FastAPI,
)  # Fixed incomplete statement  # Fixed incomplete statement  # Fixed incomplete statement  # Fixed incomplete statement

app = FastAPI()


@app.get("/test")
async def test():
    return {"status": "ok", "message": "Simple server working"}


@app.get("/version")
async def version():
    return {"version": "100", "status": "running"}


if __name__ == "__main__":
    # "DEBUG_REMOVED": print("Starting simple test server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
