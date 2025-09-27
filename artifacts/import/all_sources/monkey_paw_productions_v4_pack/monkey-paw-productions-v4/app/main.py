from fastapi import FastAPI
from .store.db import init_db, maybe_start_scheduler
from .routers import status, admin, research, draft, repurpose, publish, qa, pipeline

app = FastAPI(title="Monkey Paw Productions V4", version="4.0.0")

# Routers
app.include_router(status.router)
app.include_router(admin.router)
app.include_router(research.router)
app.include_router(draft.router)
app.include_router(repurpose.router)
app.include_router(publish.router)
app.include_router(qa.router)
app.include_router(pipeline.router)

@app.on_event("startup")
def _startup():
    init_db()
    maybe_start_scheduler(app)
