
from fastapi import APIRouter
from fastapi.responses import JSONResponse
import aiosqlite, os, time

router = APIRouter()
DB_PATH = os.environ.get("RUNTIME_DB", "backend/runtime.db")

async def ensure():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("CREATE TABLE IF NOT EXISTS metrics (name TEXT PRIMARY KEY, value REAL, updated REAL)")
        await db.execute("CREATE TABLE IF NOT EXISTS kv (key TEXT PRIMARY KEY, value TEXT)")
        await db.commit()

@router.post("/metrics/inc")
async def inc(body: dict):
    await ensure()
    name = body.get("name","")
    v = float(body.get("value", 1.0))
    now = time.time()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT INTO metrics (name,value,updated) VALUES (?,?,?) ON CONFLICT(name) DO UPDATE SET value=value+excluded.value, updated=?", (name,v,now,now))
        await db.commit()
    return {"ok": True}

@router.post("/alerts/check_error_budget")
async def check_error_budget(body: dict):
    await ensure()
    window = float(body.get("window_secs", 3600))
    budget = float(body.get("budget", 10)) # allowed failures in window
    now = time.time()
    cutoff = now - window
    # Using simple stored counter 'failures_last_hour' updated by your code
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT value FROM metrics WHERE name='failures_last_hour'")
        row = await cur.fetchone()
        fails = row[0] if row else 0
        if fails > budget:
            await db.execute("INSERT OR REPLACE INTO kv (key,value) VALUES ('PAUSE_ALL','on')")
            await db.commit()
            return {"ok": True, "paused": "ALL", "failures": fails, "budget": budget}
    return {"ok": True, "paused": "no", "budget": budget}
