from fastapi import FastAPI
from .routers import status, admin, research, draft, repurpose, publish

app = FastAPI(title="Monkey Paw — Live")

app.include_router(status.router, prefix="/api")
app.include_router(admin.router, prefix="/api/admin")
app.include_router(research.router, prefix="/api")
app.include_router(draft.router, prefix="/api")
app.include_router(repurpose.router, prefix="/api")
app.include_router(publish.router, prefix="/api")
