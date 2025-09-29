
import aiosqlite, os, time

DB_PATH = os.environ.get("RUNTIME_DB", "backend/runtime.db")

async def log(action: str, subject: str, meta: dict = None):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("CREATE TABLE IF NOT EXISTS audit (ts REAL, action TEXT, subject TEXT, meta TEXT)")
        await db.execute("INSERT INTO audit (ts,action,subject,meta) VALUES (?,?,?,?)", (time.time(), action, subject, str(meta or {})))
        await db.commit()
