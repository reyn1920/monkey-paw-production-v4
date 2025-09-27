from fastapi import FastAPI

app = FastAPI(title="Monkey Paw — Live")

@app.get("/api/health")
def health():
    return {"ok": True, "service": "monkey-paw-live", "nocode_stack_enabled": False}
