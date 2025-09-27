from sqlmodel import SQLModel, Field, create_engine, Session, select
from pathlib import Path
from typing import Optional
import datetime
from apscheduler.schedulers.background import BackgroundScheduler

DB_PATH = Path(__file__).resolve().parents[2] / "artifacts" / "monkeypaw_v4.db"
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
    avatar: str = "default"
    content: str
    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.utcnow())

class Asset(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    draft_id: int
    kind: str
    path: str
    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.utcnow())

def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as s:
        for k,v in [
            ("approve_publish","false"),
            ("scheduler_enabled","false"),
            ("last_pipeline_run","")
        ]:
            if not s.get(ConfigKV, k):
                s.add(ConfigKV(key=k, value=v))
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

_scheduler = None

def maybe_start_scheduler(app):
    global _scheduler
    if get_flag("scheduler_enabled","false") != "true":
        return
    if _scheduler: 
        return
    _scheduler = BackgroundScheduler(daemon=True)
    from ..services.pipeline_service import pipeline_heartbeat
    _scheduler.add_job(pipeline_heartbeat, 'interval', minutes=15, id="pipeline_heartbeat", replace_existing=True)
    _scheduler.start()
