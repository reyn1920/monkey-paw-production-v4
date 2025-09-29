
import re, os, json, aiosqlite
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

DB_PATH = os.environ.get("RUNTIME_DB", "backend/runtime.db")

FAILSAFE_CONFIG = {
    "WRITING":   [r"^/api/draft$", r"^/api/draft/run", r"^/api/draft/.*", r"^/api/draftmode/.*", r"^/api/writer"],
    "THUMBS":    [r"^/api/thumbs", r"^/api/publish/thumbs"],
    "CAPTIONS":  [r"^/api/captions"],
    "BUNDLER":   [r"^/api/bundle", r"^/tools/bundle"],
    "PUBLISH":   [r"^/api/publish/(?!videos|checklist)"],
    "UPLOADS":   [r"^/api/upload", r"^/api/social"],
    "SCHEDULER": [r"^/api/schedule", r"^/api/jobs"],
    "INGEST":    [r"^/api/ingest"],
    "BGRENDER":  [r"^/api/backgrounds"],
    "AVATAR":    [r"^/api/avatars", r"^/api/compose"],
}

ALLOW_ALWAYS = [
    r"^/$", r"^/health$", r"^/observer", r"^/api/observer", r"^/failsafes", r"^/api/failsafes",
    r"^/bundles", r"^/backup", r"^/api/backup", r"^/assets/", r"^/static/", r"^/board$", r"^/api/channels",
    r"^/drafts$", r"^/api/drafts", r"^/api/draftmode", r"^/backgrounds$", r"^/avatars$",
]

async def kv_get(key: str):
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            cur = await db.execute("SELECT value FROM kv WHERE key=?", (key,))
            row = await cur.fetchone()
            return row[0] if row else None
    except Exception:
        return None

class FailsafeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        method = request.method.upper()
        for pat in ALLOW_ALWAYS:
            if re.match(pat, path):
                return await call_next(request)

        if os.environ.get("PAUSE_ALL", "").lower() in ("1","true","yes","on"):
            if method in ("POST","PUT","DELETE"):
                return JSONResponse({"ok": False, "paused": "ALL (env)"}, status_code=503)

        gv = await kv_get("PAUSE_ALL")
        if gv and gv.lower() in ("1","true","yes","on"):
            if method in ("POST","PUT","DELETE"):
                return JSONResponse({"ok": False, "paused": "ALL"}, status_code=503)

        if method in ("POST","PUT","DELETE"):
            for name, patterns in FAILSAFE_CONFIG.items():
                flag = await kv_get(f"PAUSE_{name}")
                if flag and flag.lower() in ("1","true","yes","on"):
                    for pat in patterns:
                        if re.match(pat, path):
                            return JSONResponse({"ok": False, "paused": name}, status_code=503)
        return await call_next(request)
