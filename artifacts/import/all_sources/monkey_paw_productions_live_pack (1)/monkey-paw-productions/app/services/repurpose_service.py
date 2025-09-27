from sqlmodel import Session
from pathlib import Path
from ..store.db import Asset, engine
import datetime, json

ART_DIR = Path(__file__).resolve().parents[2] / "artifacts" / "staging"

def save_asset(draft_id: int, kind: str, content: str) -> str:
    ART_DIR.mkdir(parents=True, exist_ok=True)
    path = ART_DIR / f"{kind}_{draft_id}.txt"
    path.write_text(content)
    with Session(engine) as s:
        a = Asset(draft_id=draft_id, kind=kind, path=str(path), created_at=datetime.datetime.utcnow())
        s.add(a); s.commit()
    return str(path)
