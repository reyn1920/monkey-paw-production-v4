# utils/seed_sqlite.py
import os
import asyncio
import aiosqlite

DB_PATH = os.getenv("DB_PATH", "data/base44.sqlite")
SEEDS = [
    (
        "evergreen niches",
        "how-to, personal finance, home hacks, study skills, ocean ambience",
    ),
    ("initial channels", "Channel-A, Channel-B, Channel-C, Channel-D"),
    ("workflow", "research -> write -> voice -> avatar -> edit -> publish -> track"),
]


async def main():
    import os

    os.makedirs("data", exist_ok=True)
    async with aiosqlite.connect(DB_PATH) as db:
        for t, d in SEEDS:
            await db.execute("INSERT INTO seeds(topic, details) VALUES(?,?)", (t, d))
        await db.commit()
    print("Seeded:", len(SEEDS))


if __name__ == "__main__":
    asyncio.run(main())
