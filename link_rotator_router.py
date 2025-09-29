
from fastapi import APIRouter
from fastapi.responses import JSONResponse
import aiosqlite, os, random, urllib.parse, time

router = APIRouter()
DB_PATH = os.environ.get("RUNTIME_DB", "backend/runtime.db")

async def ensure():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("CREATE TABLE IF NOT EXISTS links (group_name TEXT, url TEXT, weight REAL DEFAULT 1.0)")
        await db.execute("CREATE TABLE IF NOT EXISTS clicks (group_name TEXT, url TEXT, ts REAL)")
        await db.commit()

def add_utm(url: str, source: str, campaign: str):
    u = list(urllib.parse.urlparse(url))
    q = dict(urllib.parse.parse_qsl(u[4]))
    q.update({"utm_source": source, "utm_campaign": campaign})
    u[4] = urllib.parse.urlencode(q)
    return urllib.parse.urlunparse(u)

@router.post("/links/add")
async def add_link(body: dict):
    await ensure()
    g = body.get("group"); url = body.get("url"); w = float(body.get("weight",1.0))
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT INTO links (group_name,url,weight) VALUES (?,?,?)",(g,url,w)); await db.commit()
    return {"ok": True}

@router.get("/links/resolve")
async def resolve(group: str, source: str = "youtube", campaign: str = "default"):
    await ensure()
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT url, weight FROM links WHERE group_name=?", (group,))
        rows = await cur.fetchall()
    if not rows: return {"ok": False, "error": "no links for group"}
    # weighted choice
    total = sum(w for _,w in rows)
    r = random.uniform(0,total); upto = 0.0
    for url,w in rows:
        if upto + w >= r:
            final = add_utm(url, source, campaign)
            async with aiosqlite.connect(DB_PATH) as db:
                await db.execute("INSERT INTO clicks (group_name,url,ts) VALUES (?,?,?)",(group,final,time.time())); await db.commit()
            return {"ok": True, "url": final}
        upto += w
    return {"ok": True, "url": add_utm(rows[0][0], source, campaign)}
