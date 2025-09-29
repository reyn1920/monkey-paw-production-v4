from fastapi import APIRouter
from pydantic import BaseModel
import os
import sqlite3
from typing import Optional

DB_PATH = os.environ.get(
    "TRAE_DB_PATH", os.path.join(os.getcwd(), "data", "trae_ai.db")
)
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

router = APIRouter()


class ToggleIn(BaseModel):
    channel_id: str
    live_on: Optional[bool] = None
    auto_on: Optional[bool] = None
    review_required: Optional[bool] = None
    humanize_web_on: Optional[bool] = None


def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _init():
    conn = _connect()
    cur = conn.cursor()
    cur.execute(
        """
    CREATE TABLE IF NOT EXISTS automation_toggles (
        channel_id TEXT PRIMARY KEY,
        live_on INTEGER DEFAULT 0,
        auto_on INTEGER DEFAULT 0,
        review_required INTEGER DEFAULT 1,
        humanize_web_on INTEGER DEFAULT 1,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """
    )
    conn.commit()
    conn.close()


_init()


@router.get("/toggles")
def get_toggles(channel_id: str):
    conn = _connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM automation_toggles WHERE channel_id = ?", (channel_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return {
            "channel_id": channel_id,
            "live_on": False,
            "auto_on": False,
            "review_required": True,
            "humanize_web_on": True,
        }
    return dict(row)


@router.post("/toggles")
def set_toggles(data: ToggleIn):
    conn = _connect()
    cur = conn.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO automation_toggles(channel_id) VALUES(?)",
        (data.channel_id,),
    )
    for field in ["live_on", "auto_on", "review_required", "humanize_web_on"]:
        val = getattr(data, field)
        if val is not None:
            cur.execute(
                f"UPDATE automation_toggles SET {field}=?, updated_at=CURRENT_TIMESTAMP WHERE channel_id=?",
                (1 if val else 0, data.channel_id),
            )
    conn.commit()
    conn.close()
    return {"ok": True}
