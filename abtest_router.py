
from fastapi import APIRouter
from fastapi.responses import JSONResponse
import aiosqlite, os, math, time, json

router = APIRouter()
DB_PATH = os.environ.get("RUNTIME_DB", "backend/runtime.db")

async def ensure():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("CREATE TABLE IF NOT EXISTS experiments (name TEXT, variant TEXT, shows INTEGER DEFAULT 0, rewards REAL DEFAULT 0.0, PRIMARY KEY (name, variant))")
        await db.commit()

@router.post("/ab/choose")
async def choose(body: dict):
    await ensure()
    name = body.get("name","")
    variants = body.get("variants") or []
    if not name or not variants:
        return JSONResponse({"ok": False, "error": "name and variants required"}, status_code=400)
    async with aiosqlite.connect(DB_PATH) as db:
        total = 0
        scores = []
        for v in variants:
            cur = await db.execute("SELECT shows, rewards FROM experiments WHERE name=? AND variant=?", (name, v))
            row = await cur.fetchone()
            if not row:
                await db.execute("INSERT OR IGNORE INTO experiments (name, variant, shows, rewards) VALUES (?,?,0,0.0)", (name,v))
                shows, rewards = 0, 0.0
            else:
                shows, rewards = row
            total += max(shows,1)
        # UCB1 score
        best = None; best_v = variants[0]
        for v in variants:
            cur = await db.execute("SELECT shows, rewards FROM experiments WHERE name=? AND variant=?", (name, v))
            row = await cur.fetchone(); shows, rewards = (row or (0,0.0))
            avg = (rewards / shows) if shows>0 else 0.0
            score = avg + math.sqrt(2*math.log(max(total,1))/max(shows,1))
            if best is None or score > best:
                best = score; best_v = v
        await db.commit()
    return {"ok": True, "variant": best_v}

@router.post("/ab/report")
async def report(body: dict):
    await ensure()
    name = body.get("name","")
    variant = body.get("variant","")
    reward = float(body.get("reward", 0.0))
    if not name or not variant:
        return JSONResponse({"ok": False, "error": "name and variant required"}, status_code=400)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT OR IGNORE INTO experiments (name, variant, shows, rewards) VALUES (?,?,0,0.0)", (name,variant))
        await db.execute("UPDATE experiments SET shows=shows+1, rewards=rewards+? WHERE name=? AND variant=?", (reward, name, variant))
        await db.commit()
    return {"ok": True}
