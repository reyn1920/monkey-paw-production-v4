
import time, aiosqlite, os
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

DB_PATH = os.environ.get("RUNTIME_DB", "backend/runtime.db")

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, limits=None):
        super().__init__(app)
        self.limits = limits or {
            "/api/backgrounds/render": (5, 60),  # 5 renders/min
            "/api/compose/preview": (30, 60)     # 30 previews/min
        }

    async def dispatch(self, request, call_next):
        path = request.url.path
        if path in self.limits and request.method.upper()=="POST":
            limit, window = self.limits[path]
            now = time.time()
            async with aiosqlite.connect(DB_PATH) as db:
                await db.execute("CREATE TABLE IF NOT EXISTS ratelimits (path TEXT, ts REAL)")
                await db.execute("DELETE FROM ratelimits WHERE ts < ?", (now-window,))
                await db.execute("INSERT INTO ratelimits (path, ts) VALUES (?,?)", (path, now))
                await db.commit()
                cur = await db.execute("SELECT COUNT(*) FROM ratelimits WHERE path=? AND ts>=?", (path, now-window))
                n = (await cur.fetchone())[0]
                if n > limit:
                    return JSONResponse({"ok": False, "error": "rate_limited", "path": path}, status_code=429)
        return await call_next(request)
