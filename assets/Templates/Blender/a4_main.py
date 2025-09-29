# fastapi_app/main.py — Base44 backend (Rule‑1 compliant)
import os
from typing import Any
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from starlette.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import aiosqlite

APP_PORT = int(os.getenv("APP_PORT", "8099"))
DB_PATH = os.getenv("DB_PATH", "data/base44.sqlite")

app = FastAPI(title="Base44 Runtime API", version="1.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def db_init():
    os.makedirs("data", exist_ok=True)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executescript(
            """
            CREATE TABLE IF NOT EXISTS settings(
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS channels(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                notes TEXT DEFAULT ""
            );
            CREATE TABLE IF NOT EXISTS seeds(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                details TEXT DEFAULT ""
            );
            CREATE TABLE IF NOT EXISTS state(
                key TEXT PRIMARY KEY,
                value INTEGER NOT NULL
            );
            CREATE TABLE IF NOT EXISTS streams(
                name TEXT PRIMARY KEY,
                enabled INTEGER NOT NULL DEFAULT 0
            );
            """
        )
        # defaults
        await db.execute("INSERT OR IGNORE INTO state(key,value) VALUES('go_live',0)")
        await db.execute(
            "INSERT OR IGNORE INTO state(key,value) VALUES('automation',0)"
        )
        for s in (
            "youtube",
            "books",
            "digital_products",
            "affiliate",
            "podcast",
            "courses",
            "print_on_demand",
        ):
            await db.execute(
                "INSERT OR IGNORE INTO streams(name,enabled) VALUES(?,0)", (s,)
            )
        await db.commit()


@app.on_event("startup")
async def on_start():
    await db_init()


@app.get("/health")
async def health() -> dict[str, Any]:
    return {"ok": True, "service": "base44", "db": DB_PATH}


class ChannelIn(BaseModel):
    name: str
    notes: str = ""


@app.post("/channels")
async def create_channel(ch: ChannelIn):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO channels(name, notes) VALUES(?,?)", (ch.name, ch.notes)
        )
        await db.commit()
    return {"ok": True}


@app.get("/channels")
async def list_channels():
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT id,name,notes FROM channels ORDER BY id DESC")
        rows = await cur.fetchall()
    return [{"id": r[0], "name": r[1], "notes": r[2]} for r in rows]


@app.get("/state")
async def get_state():
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT key,value FROM state")
        m = {k: bool(v) for (k, v) in await cur.fetchall()}
    return m


class StateIn(BaseModel):
    go_live: bool | None = None
    automation: bool | None = None


@app.post("/state")
async def set_state(s: StateIn):
    async with aiosqlite.connect(DB_PATH) as db:
        if s.go_live is not None:
            await db.execute(
                "INSERT OR REPLACE INTO state(key,value) VALUES('go_live',?)",
                (1 if s.go_live else 0,),
            )
        if s.automation is not None:
            await db.execute(
                "INSERT OR REPLACE INTO state(key,value) VALUES('automation',?)",
                (1 if s.automation else 0,),
            )
        await db.commit()
    return {"ok": True}


@app.get("/streams")
async def get_streams():
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT name,enabled FROM streams ORDER BY name")
        rows = await cur.fetchall()
    return [{"name": r[0], "enabled": bool(r[1])} for r in rows]


class StreamIn(BaseModel):
    enabled: bool


@app.post("/streams/{name}")
async def set_stream(name: str, body: StreamIn):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR REPLACE INTO streams(name,enabled) VALUES(?,?)",
            (name, 1 if body.enabled else 0),
        )
        await db.commit()
    return {"ok": True}


# static dashboard
if os.path.isdir("frontend/dist"):
    app.mount(
        "/dashboard_assets",
        StaticFiles(directory="frontend/dist", html=False),
        name="dashboard_assets",
    )


@app.get("/dashboard")
async def dashboard_index():
    p = "frontend/dist/index.html"
    if os.path.isfile(p):
        return FileResponse(p)
    return JSONResponse(
        {
            "ok": False,
            "hint": "Build frontend first: cd frontend && npm install && npm run build",
        },
        status_code=404,
    )
