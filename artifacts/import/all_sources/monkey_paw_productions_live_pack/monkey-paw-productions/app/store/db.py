from sqlmodel import SQLModel, Field, create_engine, Session, select
from pathlib import Path
from typing import Optional
import datetime, json

DB_PATH = Path(__file__).resolve().parents[2] / "artifacts" / "monkeypaw.db"
engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})

class ConfigKV(SQLModel, table=True):
    key: str = Field(primary_key=True)
    value: str

class ResearchItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    topic: str
    source: str
    content: str
    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.utcnow())

class Draft(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    research_id: int
    content: str
    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.utcnow())

class Asset(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    draft_id: int
    kind: str
    path: str
    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.utcnow())

class JobRun(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    status: str
    note: str = ""
    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.utcnow())

def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as s:
        if not s.get(ConfigKV, "approve_publish"):
            s.add(ConfigKV(key="approve_publish", value="false"))
            s.commit()

def set_flag(key: str, value: str):
    with Session(engine) as s:
        cfg = s.get(ConfigKV, key) or ConfigKV(key=key, value=value)
        cfg.value = value
        s.add(cfg); s.commit()

def get_flag(key: str, default="false"):
    with Session(engine) as s:
        cfg = s.get(ConfigKV, key)
        return cfg.value if cfg else default
