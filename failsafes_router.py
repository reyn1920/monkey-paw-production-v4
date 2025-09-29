
from fastapi import APIRouter
from fastapi.responses import JSONResponse
import aiosqlite, os

router = APIRouter()
DB_PATH = os.environ.get("RUNTIME_DB", "backend/runtime.db")

@router.post("/failsafes/set")
async def set_flag(body: dict):
    key = (body.get("key") or "").strip()
    value = (body.get("value") or "").strip()
    if not key:
        return JSONResponse({"ok": False, "error": "key required"}, status_code=400)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("CREATE TABLE IF NOT EXISTS kv (key TEXT PRIMARY KEY, value TEXT)")
        await db.execute("INSERT OR REPLACE INTO kv (key,value) VALUES (?,?)", (key, value))
        await db.commit()
    return {"ok": True, "key": key, "value": value}
