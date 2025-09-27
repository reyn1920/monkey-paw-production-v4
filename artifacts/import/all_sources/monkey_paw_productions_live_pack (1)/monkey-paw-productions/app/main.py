"""
Monkey Paw Productions — Live API
Local-first, add-only. Auto-publish locked until self-test passes and approve flag is set.
"""
from fastapi import FastAPI
from .store.db import init_db
from .routers import research, draft, repurpose, publish, status, admin

app = FastAPI(title="Monkey Paw Productions", version="1.0.0")

# Routers
app.include_router(status.router)
app.include_router(admin.router)
app.include_router(research.router)
app.include_router(draft.router)
app.include_router(repurpose.router)
app.include_router(publish.router)

@app.on_event("startup")
def on_startup():
    init_db()
