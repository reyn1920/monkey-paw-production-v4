
import asyncio, aiosqlite, os, json, time

DB_PATH = os.environ.get("RUNTIME_DB", "backend/runtime.db")

async def run_once():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("CREATE TABLE IF NOT EXISTS jobs (id INTEGER PRIMARY KEY, channel TEXT, kind TEXT, due_at TEXT, payload TEXT, status TEXT DEFAULT 'queued')")
        cur = await db.execute("SELECT id,channel,kind,payload FROM jobs WHERE status='queued' AND due_at <= datetime('now') ORDER BY id LIMIT 5")
        rows = await cur.fetchall()
        for (jid, ch, kind, payload) in rows:
            # stub: mark running -> done, real system would call bundler/writer
            await db.execute("UPDATE jobs SET status='running' WHERE id=?", (jid,))
            await asyncio.sleep(0.1)
            await db.execute("UPDATE jobs SET status='done' WHERE id=?", (jid,))
        await db.commit()

async def main():
    while True:
        await run_once()
        await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(main())
