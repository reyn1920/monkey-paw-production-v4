# -*- coding: utf-8 -*-
# flake8: noqa: E501,E402
"""
PLAN

Drop-in pack designed to merge into your existing app, not replace it.

Copy-based ingestion from Drive/Downloads/Desktop -> stage -> integrate into your current project.

Convene ChatGPT <-> Gemini button (builds pro prompt, copies to clipboard, opens both web apps).

Public/private toggle.

AI coders mutual diagnostics (two-pass plan).

VS Code integration prompt that applies this pack additively under _mp_integration/, sets tasks, and wires run/ingest/merge.

WHAT'S INSIDE

backend/ FastAPI API (health, toggle, prompt builder, audit plan).

dashboard/index.html one-user UI (ChatGPT<->Gemini, public/private, diagnostics).

merge/

merge_config.json - set your real paths here (current project + Drive/Downloads/Desktop roots).

ingest_and_stage.py - copies matched folders (Online Production/Base88/MonkeyPaw variants) into a timestamped staging area (no delete).

merge_into_current.sh - merges the latest stage into your current project under integrated_pack/<timestamp> (copy-based, backups created).

scripts/run_api.sh - start the API on 127.0.0.1:8000.

prompts/

vscode_integrate_prompt.txt - detailed prompt for VS Code to integrate this ZIP into your current app.

README.md - exact run/ingest/merge steps.

COMMANDS (quick start)
# 1) Unzip wherever you want to stage the pack
cd ~/Desktop
unzip -o ~/Downloads/monkey_paw_integration_pack_v6.zip -d monkey_paw_integration_pack_v6
cd monkey_paw_integration_pack_v6

# 2) Install deps and run API
python3 -m pip install --upgrade pip
python3 -m pip install -r backend/requirements.txt
./scripts/run_api.sh  # API at http://127.0.0.1:8000
# In Finder or Terminal:
open dashboard/index.html

# 3) Edit merge config to point to YOUR current project + sources
$EDITOR merge/merge_config.json
# - current_project_root: path to the app you’re working on now
# - import_paths: add your Google Drive path + Downloads + Desktop
# - name_filters already match: "online","production","ONLIN","Base88","Monkey","Paw", etc.

# 4) Ingest from Drive/Downloads/Desktop into a timestamped stage
python3 merge/ingest_and_stage.py

# 5) Merge the latest stage INTO your current project (copy-based, backups saved)
bash merge/merge_into_current.sh

VERIFY

Health:

curl -s http://127.0.0.1:8000/api/health


Public toggle:

curl -s -X POST http://127.0.0.1:8000/api/toggle_public \
  -H 'Content-Type: application/json' -d '{"public":true}'


Prompt builder (you can also use the dashboard UI):

curl -s -X POST http://127.0.0.1:8000/api/prompt_broker \
  -H 'Content-Type: application/json' \
  -d '{"goal":"Integrate all prior assets + upgrades into my current app and stabilize for live publish","constraints":["Rule-1 ban","No-delete","Zero-cost","M1 friendly"],"context":{"merge":"best-of-both"}}'

DETAILED PROMPT (paste into VS Code to integrate this ZIP into your current repo)
You are a professional assistant operating in VS Code on macOS (M1, 16GB). 
Goal: Integrate the attached “Monkey-Paw Integration Pack v6” into my CURRENT app additively (no deletions), then sweep/import from Google Drive + Downloads + Desktop and merge results. Keep zero-cost. Enforce Rule-1, No-Delete, and Universal Persistence Rule (two clean passes).

Follow the Base44 Output Contract:

PLAN
- Detect my active workspace as the current app. Do not move or remove files.
- Add-only: copy pack content into a new folder named _mp_integration/ at the root of the current app.
- Create `.vscode/tasks.json` with tasks:
  - “Run API” -> ./_mp_integration/scripts/run_api.sh
  - “Open Dashboard” -> open ./_mp_integration/dashboard/index.html
  - “Ingest From Sources” -> python3 ./_mp_integration/merge/ingest_and_stage.py
  - “Merge Staged Into Current” -> bash ./_mp_integration/merge/merge_into_current.sh
- Create Makefile with targets: run, ingest, merge, verify.
- Print post-steps to toggle public and use the ChatGPT<->Gemini convene flow.

DIFFS
- Add `_mp_integration/` with backend/, dashboard/, merge/, scripts/, prompts/.
- Add `.vscode/tasks.json` and `Makefile`.
- Add `README_INTEGRATION.md` summarizing the steps and safety rules.

COMMANDS
- Use copy-based commands to place all pack files under `_mp_integration/` (no overwrite outside it).
- Generate `.vscode/tasks.json` and `Makefile`.
- Run the “Run API” task then “Open Dashboard”.
- Guide me to edit `_mp_integration/merge/merge_config.json` to set:
  - current_project_root = absolute path of this workspace
  - import_paths = my Google Drive root path + Downloads + Desktop
- Run “Ingest From Sources”, then “Merge Staged Into Current”.

VERIFY
- curl http://127.0.0.1:8000/api/health -> {"status":"ok"}.
- Toggle public -> public:true shown on dashboard.
- Build prompt in the dashboard -> copied to clipboard; open both web tabs and paste.

ROLLBACK
- Remove `_mp_integration/` and folders created under `imports/`, `integrated_pack/`, `backups/` only. No other files.

Constraints:
- Rule-1 vocabulary ban in any added strings/docs.
- No-Delete: do not remove or overwrite existing app code.
- Zero-cost: do not add any paid/trial services.
- Two-pass verification before declaring done.
"""

import asyncio
import csv
import io
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional

import yaml
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

import requests


# Pydantic Models
class SheetsConfig(BaseModel):
    revenue_csv_url: Optional[str] = None
    content_kpis_csv_url: Optional[str] = None
    poll_seconds: Optional[int] = None


class SheetsFromSheet(BaseModel):
    sheet_url: str
    revenue_tab: str = "revenue_daily"
    kpis_tab: str = "content_kpis"
    poll_seconds: Optional[int] = None


class EnqueueJob(BaseModel):
    type: str
    channel: Optional[str] = None
    payload_json: Optional[dict] = None
    priority: Optional[int] = 5


class BootstrapRequest(BaseModel):
    channel: Optional[str] = None
    videos: int = 6
    shorts: int = 3


BASE = Path(__file__).resolve().parents[1]
REPORTS = BASE / "reports"
APPROVAL = REPORTS / "approve_publish.true"
ART_STAGING = BASE / "artifacts" / "staging"
ART_PUBLISHED = BASE / "artifacts" / "published"
SHEETS_CONFIG = BASE / "config" / "sheets.yaml"
LAST_REFRESH_FILE = BASE / "out" / "last_refresh.txt"
DB_MAIN = BASE / "out" / "main.db"
INGEST_RULES_YAML = BASE / "config" / "ingest_rules.yaml"

# External Web Guard pack (installed add-only under Desktop)
PACK_DIR = Path.home() / "Desktop" / "monkey-paw" / "_mp_maxout_stack"
PACK_VENV_PY = PACK_DIR / ".venv" / "bin" / "python"
GUARD_SCRIPT = PACK_DIR / "tools" / "web_access_guard.py"
GUARD_LOG = PACK_DIR / "logs" / "web_access_guard.log"
RUNTIME_YML = PACK_DIR / "config" / "runtime.yml"
LAUNCH_AGENT = Path.home() / "Library" / "LaunchAgents" / "com.monkeypaw.webguard.plist"

# Integrations config (Trae.ai token, Downloads path, Drive path)
INTEGRATIONS_YAML = BASE / "config" / "integrations.yaml"

# Import routers (support both package and script contexts)
try:
    # Prefer absolute package imports so internal relative imports (..foo) work
    from app.routers import sheets_router, trae_ai_router
    from app.routers.ai_systems_status import router as ai_systems_router
    from app.routers.websocket_simple import router as websocket_router
    from app.routers.integration_pack import router as integration_pack_router
    from app.routers.integration_pack_public import router as integration_pack_public_router
except ImportError:
    try:
        # When executed as a package: uvicorn app.main:app
        from .routers import sheets_router, trae_ai_router
        from .routers.ai_systems_status import router as ai_systems_router
        from .routers.websocket_simple import router as websocket_router
        from .routers.integration_pack import router as integration_pack_router
        from .routers.integration_pack_public import router as integration_pack_public_router
    except ImportError:
        # Last resort: direct module-level imports
        from routers import sheets_router, trae_ai_router
        from routers.ai_systems_status import router as ai_systems_router
        from routers.websocket_simple import router as websocket_router
        from routers.integration_pack import router as integration_pack_router
        from routers.integration_pack_public import router as integration_pack_public_router

templates = Jinja2Templates(directory=str(BASE / "app" / "templates"))
app = FastAPI(title="Monkey Paw — V4", version="4.0.0")
app.add_middleware(GZipMiddleware, minimum_size=500)
app.mount("/static", StaticFiles(directory=str(BASE / "app" / "static")), name="static")

# Silence linter F401 for intentionally-imported helpers used by runtime wiring
_unused = (os, List, WebSocket, WebSocketDisconnect)  # noqa: F401

# Include routers
app.include_router(sheets_router.router)
app.include_router(trae_ai_router.router)
app.include_router(ai_systems_router)
app.include_router(websocket_router)
app.include_router(integration_pack_router)
app.include_router(integration_pack_public_router)

# CORS for common dev origins (adjust as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def db_conn():
    # Ensure DB directory exists before connecting
    try:
        DB_MAIN.parent.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass
    con = sqlite3.connect(str(DB_MAIN), timeout=5.0, check_same_thread=False)
    try:
        con.execute("PRAGMA journal_mode=WAL;")
        con.execute("PRAGMA synchronous=NORMAL;")
        con.execute("PRAGMA busy_timeout=5000;")
    except Exception:
        pass
    return con


def ensure_schema():
    con = db_conn()
    cur = con.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS revenue_daily (
            day TEXT PRIMARY KEY,
            goal REAL,
            actual REAL
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS content_kpis (
            metric TEXT PRIMARY KEY,
            value INTEGER
        )
        """
    )
    pol = read_policy()
    # Registry of imported datasets (read-only usage inside app)
    if pol.get("enable_datasets_registry", True):
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS datasets_registry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                path TEXT NOT NULL,
                kind TEXT NOT NULL,
                note TEXT,
                imported_at REAL NOT NULL
            )
            """
        )
    # Voice registry (normalized view of available voices)
    if pol.get("enable_voices_registry", True):
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS voices_registry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                provider TEXT NOT NULL,
                voice_name TEXT NOT NULL,
                language TEXT,
                gender TEXT,
                quality TEXT,
                path TEXT,
                meta_json TEXT,
                active INTEGER NOT NULL DEFAULT 1,
                UNIQUE(provider, voice_name)
            )
            """
        )
    # Jobs system
    if pol.get("enable_jobs", True):
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                channel TEXT,
                payload_json TEXT,
                status TEXT NOT NULL DEFAULT 'queued',
                priority INTEGER NOT NULL DEFAULT 5,
                retries INTEGER NOT NULL DEFAULT 0,
                next_run_at REAL,
                created_at REAL NOT NULL,
                updated_at REAL NOT NULL
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS job_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id INTEGER NOT NULL,
                ts REAL NOT NULL,
                level TEXT NOT NULL,
                message TEXT NOT NULL,
                data_json TEXT,
                FOREIGN KEY(job_id) REFERENCES jobs(id)
            )
            """
        )
        # Daily shorts log to ensure we don't exceed per-day quotas
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS daily_shorts_log (
                channel TEXT NOT NULL,
                day TEXT NOT NULL,
                count INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY(channel, day)
            )
            """
        )
    # Daily niches list (top N niches per day, add-only)
    if pol.get("enable_niches", True):
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS niches_top (
                day TEXT PRIMARY KEY,
                year INTEGER NOT NULL,
                next_year INTEGER NOT NULL,
                niches_json TEXT NOT NULL
            )
            """
        )
    con.commit()
    con.close()


# ------------------------
# Drive catalog (Google Drive local sync) — add-only integration
# ------------------------

def _integrations_drive_root() -> Path:
    try:
        data = yaml.safe_load(INTEGRATIONS_YAML.read_text()) if INTEGRATIONS_YAML.exists() else {}
    except Exception:
        data = {}
    p = (data or {}).get("drive_path") or ""
    if not p:
        return Path("")
    return Path(p).expanduser()


def _ensure_drive_schema():
    con = db_conn()
    cur = con.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS drive_catalog (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            root TEXT NOT NULL,
            rel TEXT NOT NULL,
            abs_path TEXT NOT NULL,
            size INTEGER NOT NULL,
            mtime REAL NOT NULL,
            ext TEXT,
            scanned_at REAL NOT NULL,
            UNIQUE(source, root, rel)
        )
        """
    )
    con.commit()
    con.close()


@app.post("/api/drive/scan")
def drive_scan(max_files: int = 5000):
    """Scan the configured Google Drive root and upsert file metadata into SQLite.
    Uses add-only semantics. Limits to max_files to stay responsive on M1.
    """
    root = _integrations_drive_root()
    if not root or not root.exists():
        return {"ok": False, "error": f"drive root not found: {root}"}
    try:
        max_files = max(1, min(200000, int(max_files)))
    except Exception:
        max_files = 5000
    _ensure_drive_schema()
    con = db_conn()
    cur = con.cursor()
    now = time.time()
    count = 0
    for dirpath, dirnames, filenames in os.walk(root):
        # Skip hidden dirs to reduce noise
        base = os.path.basename(dirpath)
        if base.startswith('.'):
            continue
        for fn in filenames:
            if count >= max_files:
                break
            try:
                p = Path(dirpath) / fn
                if not p.is_file():
                    continue
                st = p.stat()
                rel = str(p.relative_to(root))
                ext = p.suffix.lower().lstrip('.')
                cur.execute(
                    """
                    INSERT OR REPLACE INTO drive_catalog
                    (source,root,rel,abs_path,size,mtime,ext,scanned_at)
                    VALUES (?,?,?,?,?,?,?,?)
                    """,
                    (
                        "drive",
                        str(root),
                        rel,
                        str(p),
                        int(st.st_size),
                        float(st.st_mtime),
                        ext,
                        now,
                    ),
                )
                count += 1
            except Exception:
                continue
        if count >= max_files:
            break
    con.commit()
    con.close()
    return {"ok": True, "indexed": count, "root": str(root)}


@app.get("/api/drive/list")
def drive_list(q: str = "", ext: str = "", limit: int = 200, offset: int = 0, sort: str = "mtime_desc"):
    _ensure_drive_schema()
    con = db_conn()
    cur = con.cursor()
    limit = max(1, min(1000, int(limit)))
    offset = max(0, int(offset))
    where = ["source='drive'"]
    args: list = []
    if q:
        where.append("rel LIKE ?")
        args.append(f"%{q}%")
    if ext:
        where.append("ext = ?")
        args.append(ext.lower())
    order = {
        "mtime_desc": "mtime DESC",
        "mtime_asc": "mtime ASC",
        "size_desc": "size DESC",
        "size_asc": "size ASC",
        "name": "rel ASC",
    }.get(sort, "mtime DESC")
    sql = f"SELECT rel,size,mtime,ext FROM drive_catalog WHERE {' AND '.join(where)} ORDER BY {order} LIMIT ? OFFSET ?"
    cur.execute(sql, (*args, limit, offset))
    rows = cur.fetchall()
    # count total for pager
    cur.execute(f"SELECT COUNT(1) FROM drive_catalog WHERE {' AND '.join(where)}", tuple(args))
    total = int(cur.fetchone()[0])
    con.close()
    items = [
        {"rel": r[0], "size": int(r[1]), "mtime": float(r[2]), "ext": r[3] or ""}
        for r in rows
    ]
    return {"ok": True, "total": total, "limit": limit, "offset": offset, "items": items}


@app.get("/api/drive/stats")
def drive_stats():
    _ensure_drive_schema()
    con = db_conn()
    cur = con.cursor()
    cur.execute("SELECT COUNT(1), COALESCE(SUM(size),0), COALESCE(MAX(mtime),0) FROM drive_catalog WHERE source='drive'")
    count, total_size, max_mtime = cur.fetchone()
    cur.execute("SELECT ext, COUNT(1) FROM drive_catalog WHERE source='drive' GROUP BY ext ORDER BY COUNT(1) DESC LIMIT 50")
    by_ext = [{"ext": e or "", "count": c} for e, c in cur.fetchall()]
    con.close()
    return {
        "ok": True,
        "count": int(count or 0),
        "total_size": int(total_size or 0),
        "latest_mtime": float(max_mtime or 0.0),
        "by_ext": by_ext,
    }


@app.get("/api/drive/changes")
def drive_changes(since: float = 0.0, limit: int = 500):
    """List files changed since a timestamp (based on scanned_at or mtime)."""
    _ensure_drive_schema()
    con = db_conn()
    cur = con.cursor()
    limit = max(1, min(2000, int(limit)))
    cur.execute(
        """
        SELECT rel,size,mtime,ext,scanned_at
        FROM drive_catalog
        WHERE source='drive' AND (scanned_at > ? OR mtime > ?)
        ORDER BY scanned_at DESC
        LIMIT ?
        """,
        (float(since), float(since), limit),
    )
    rows = cur.fetchall()
    con.close()
    return {
        "ok": True,
        "since": float(since),
        "items": [
            {"rel": r[0], "size": int(r[1]), "mtime": float(r[2]), "ext": r[3] or "", "scanned_at": float(r[4])}
            for r in rows
        ],
    }


def _read_ingest_rules() -> dict:
    try:
        if INGEST_RULES_YAML.exists():
            return yaml.safe_load(INGEST_RULES_YAML.read_text()) or {}
    except Exception:
        pass
    # seed defaults
    return {
        "rules": [
            {"match_ext": ["pdf"], "dest_subdir": "docs"},
            {"match_ext": ["mp4", "mov"], "dest_subdir": "media"},
            {"match_ext": ["md", "txt"], "dest_subdir": "notes"},
        ]
    }


def _write_ingest_rules(cfg: dict) -> dict:
    INGEST_RULES_YAML.parent.mkdir(parents=True, exist_ok=True)
    INGEST_RULES_YAML.write_text(yaml.safe_dump(cfg, sort_keys=False))
    return cfg


@app.get("/api/drive/ingest_rules")
def drive_ingest_rules_get():
    return {"ok": True, "config": _read_ingest_rules()}


class IngestRulesUpdate(BaseModel):
    rules: List[dict]


@app.post("/api/drive/ingest_rules")
def drive_ingest_rules_post(cfg: IngestRulesUpdate):
    data = {"rules": cfg.rules or []}
    return {"ok": True, "config": _write_ingest_rules(data)}


@app.post("/api/drive/run_rules")
def drive_run_rules(limit: int = 1000):
    """Apply ingest rules to drive_catalog and copy matching files into staging subfolders."""
    rules = _read_ingest_rules().get("rules", [])
    if not rules:
        return {"ok": False, "error": "no rules"}
    _ensure_drive_schema()
    con = db_conn()
    cur = con.cursor()
    cur.execute("SELECT rel,ext FROM drive_catalog WHERE source='drive' LIMIT ?", (max(1, min(50000, int(limit))),))
    rows = cur.fetchall()
    con.close()
    cfg = _read_integrations()
    root = Path(cfg.get("drive_path") or "")
    if not root.exists():
        return {"ok": False, "error": f"drive root not found: {root}"}
    ART_STAGING.mkdir(parents=True, exist_ok=True)
    applied = []
    for rel, ext in rows:
        ext = (ext or "").lower()
        for rule in rules:
            exts = [e.lower() for e in rule.get("match_ext", [])]
            if exts and ext not in exts:
                continue
            dest_subdir = (rule.get("dest_subdir") or "").strip() or "misc"
            src = root / rel
            if not src.exists() or not src.is_file():
                break
            dest_dir = ART_STAGING / dest_subdir
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest = dest_dir / src.name
            try:
                if dest.exists():
                    dest = dest_dir / f"{int(time.time())}_{src.name}"
                dest.write_bytes(src.read_bytes())
                applied.append({"rel": rel, "rule": rule})
            except Exception:
                pass
            break  # stop at first matching rule
    return {"ok": True, "applied": applied, "staging": str(ART_STAGING)}


class DriveIngestReq(BaseModel):
    rels: List[str]


@app.post("/api/drive/ingest_from_catalog")
def drive_ingest_from_catalog(req: DriveIngestReq):
    """Copy selected Drive catalog items into artifacts/staging (add-only)."""
    _ensure_drive_schema()
    ART_STAGING.mkdir(parents=True, exist_ok=True)
    con = db_conn()
    cur = con.cursor()
    copied: list[str] = []
    for rel in (req.rels or [])[:500]:
        try:
            cur.execute(
                "SELECT abs_path FROM drive_catalog WHERE source='drive' AND rel=?",
                (rel,),
            )
            row = cur.fetchone()
            if not row:
                continue
            src = Path(row[0])
            if not src.exists() or not src.is_file():
                continue
            dest = ART_STAGING / src.name
            if dest.exists():
                dest = ART_STAGING / f"{int(time.time())}_{src.name}"
            dest.write_bytes(src.read_bytes())
            copied.append(dest.name)
        except Exception:
            continue
    con.close()
    return {"ok": True, "copied": copied, "staging": str(ART_STAGING)}


# ------------------------
# Verifiers and incidents (no auth; local only)
# ------------------------

def _staging_write_check() -> bool:
    try:
        ART_STAGING.mkdir(parents=True, exist_ok=True)
        p = ART_STAGING / ("verify_" + str(int(time.time())) + ".chk")
        p.write_text("ok")
        return True
    except Exception:
        return False


@app.get("/api/verify/live_lane")
def verify_live_lane():
    """Live-lane check: app health, guard presence, and imports list working."""
    try:
        # A) App health
        r1 = requests.get("http://127.0.0.1:8001/api/health", timeout=3)
        ok_health = r1.status_code == 200
    except Exception:
        ok_health = False
    try:
        # B) Guard status (either launchctl_loaded true or log exists)
        r2 = requests.get("http://127.0.0.1:8001/api/guard/status", timeout=3)
        g = r2.json() if r2.status_code == 200 else {}
        ok_guard = bool(g.get("launchctl_loaded") or g.get("log_exists"))
    except Exception:
        ok_guard = False
    try:
        # C) Imports list (downloads) basic call
        r3 = requests.get(
            "http://127.0.0.1:8001/api/imports/list",
            params={"source": "downloads", "glob": "**/*"},
            timeout=6,
        )
        ok_imports = r3.status_code == 200 and isinstance(r3.json().get("count", 0), int)
    except Exception:
        ok_imports = False
    return {"ok": bool(ok_health and ok_guard and ok_imports), "health": ok_health, "guard": ok_guard, "imports": ok_imports}


@app.get("/api/verify/triple")
def verify_triple():
    """Triple verify: live-lane + aux health + staging write-check."""
    try:
        lane = verify_live_lane()
    except Exception:
        lane = {"ok": False}
    try:
        aux = requests.get("http://127.0.0.1:8010/health", timeout=3)
        ok_aux = aux.status_code == 200
    except Exception:
        ok_aux = False
    ok_write = _staging_write_check()
    ok = bool(lane.get("ok") and ok_aux and ok_write)
    return {"ok": ok, "live_lane": lane, "aux": ok_aux, "staging_write": ok_write}


@app.get("/api/incidents/open")
def incidents_open():
    """List open incidents from the RCA ledger if present."""
    rca = Path.home() / "Desktop" / "monkey-paw" / "_mp_rca_pack" / "rca" / "incident_ledger.json"
    try:
        if not rca.exists():
            return {"ok": True, "items": []}
        data = json.loads(rca.read_text(errors="replace") or "[]")
        items = [x for x in (data if isinstance(data, list) else []) if str(x.get("status","open")).lower() in ("open","new","triage")]
        return {"ok": True, "items": items}
    except Exception as e:
        return {"ok": False, "error": str(e), "items": []}

def read_sheets_config():
    try:
        data = yaml.safe_load(SHEETS_CONFIG.read_text())
    except FileNotFoundError:
        data = {}
    data = data or {}
    return {
        "revenue_csv_url": data.get("revenue_csv_url", ""),
        "content_kpis_csv_url": data.get("content_kpis_csv_url", ""),
        "poll_seconds": int(data.get("poll_seconds", 60) or 60),
    }


def write_sheets_config(cfg: dict):
    SHEETS_CONFIG.parent.mkdir(parents=True, exist_ok=True)
    SHEETS_CONFIG.write_text(yaml.safe_dump(cfg, sort_keys=False))


POLICY_FILE = BASE / "config" / "policy.yaml"


def read_policy():
    """Read governance policy; provide strict defaults if missing.
    This encodes: free-only, do-not-delete, owner approval for stack changes, and allowed/disallowed components.
    """
    defaults = {
        "free_only": True,
        "do_not_delete": True,
        "stack_changes_require_owner_approval": True,
        "allow_ollama": True,
        "strict_no_warnings": True,
        "disallow_in_app_stack": ["vscode", "cursor", "firebase"],
        "notes": "Runtime tools on this Mac are fine, but do not bake disallowed items into the app stack.",
        # Feature flags
        "enable_jobs": True,
        "enable_shorts_scheduler": True,
        "enable_niches": True,
        "enable_datasets_registry": True,
        "enable_voices_registry": True,
    }
    try:
        data = yaml.safe_load(POLICY_FILE.read_text()) or {}
    except FileNotFoundError:
        data = {}
    # Merge with defaults, defaults take effect when keys missing
    for k, v in defaults.items():
        data.setdefault(k, v)
    return data


def refresh_from_sheets():
    cfg = read_sheets_config()
    rev_url = (cfg.get("revenue_csv_url") or "").strip()
    kpi_url = (cfg.get("content_kpis_csv_url") or "").strip()
    updated = {"revenue": 0, "kpis": 0}

    if not (rev_url or kpi_url):
        return {"skipped": True, **updated}

    con = db_conn()
    cur = con.cursor()
    # Revenue
    if rev_url:
        r = requests.get(rev_url, timeout=15)
        r.raise_for_status()
        reader = csv.DictReader(io.StringIO(r.text))
        for row in reader:
            day = row.get("day") or row.get("date") or row.get("Day") or row.get("Date")
            goal = row.get("goal") or row.get("Goal")
            actual = row.get("actual") or row.get("Actual")
            if not day:
                continue
            try:
                g = float(goal) if goal not in (None, "") else 0.0
                a = float(actual) if actual not in (None, "") else 0.0
            except Exception:
                g = 0.0
                a = 0.0
            cur.execute(
                "INSERT OR REPLACE INTO revenue_daily(day,goal,actual) VALUES (?,?,?)",
                (str(day), g, a),
            )
            updated["revenue"] += 1

    # KPIs
    if kpi_url:
        r = requests.get(kpi_url, timeout=15)
        r.raise_for_status()
        reader = csv.DictReader(io.StringIO(r.text))
        for row in reader:
            metric = row.get("metric") or row.get("Metric")
            value = row.get("value") or row.get("Value")
            if not metric:
                continue
            try:
                v = int(float(value)) if value not in (None, "") else 0
            except Exception:
                v = 0
            cur.execute(
                "INSERT OR REPLACE INTO content_kpis(metric,value) VALUES (?,?)",
                (str(metric), v),
            )
            updated["kpis"] += 1

    con.commit()
    con.close()
    # write last refresh timestamp (local time)
    try:
        LAST_REFRESH_FILE.parent.mkdir(parents=True, exist_ok=True)
        LAST_REFRESH_FILE.write_text(datetime.now().isoformat())
    except Exception:
        pass
    return updated


@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    response.headers.setdefault(
        "Strict-Transport-Security", "max-age=63072000; includeSubDomains; preload"
    )
    return response


@app.on_event("startup")
async def on_startup():
    ensure_schema()
    cfg = read_sheets_config()

    if cfg.get("revenue_csv_url") or cfg.get("content_kpis_csv_url"):

        async def poll_loop():
            while True:
                try:
                    refresh_from_sheets()
                except Exception as e:
                    print("sheets refresh error:", e)
                await asyncio.sleep(max(10, int(cfg.get("poll_seconds", 60) or 60)))

        asyncio.create_task(poll_loop())

    # Start background worker and schedulers (gated by policy flags)
    pol = read_policy()

    async def worker_loop():
        backoff = 1
        while True:
            try:
                ran = await asyncio.to_thread(process_one_job)
                if not ran:
                    await asyncio.sleep(min(5, backoff))
                    backoff = min(30, backoff + 1)
                else:
                    backoff = 1
            except Exception as e:
                print("worker error:", e)
                await asyncio.sleep(5)

    if pol.get("enable_jobs", True):
        asyncio.create_task(worker_loop())
    # Start shorts scheduler
    if pol.get("enable_shorts_scheduler", True):
        asyncio.create_task(shorts_scheduler_loop())
    # Start niches scheduler
    if pol.get("enable_niches", True):
        asyncio.create_task(niches_scheduler_loop())

    # Schedule nightly Drive scan at ~02:30 local, chunked
    async def drive_scan_scheduler():
        while True:
            try:
                # compute seconds until next 02:30
                now = datetime.now()
                target = now.replace(hour=2, minute=30, second=0, microsecond=0)
                if target <= now:
                    target = target + timedelta(days=1)
                await asyncio.sleep((target - now).total_seconds())
                # Run chunked scans to limit resource use
                await asyncio.to_thread(lambda: drive_scan(max_files=25000))
            except Exception as e:
                print("drive scan scheduler error:", e)
                await asyncio.sleep(300)

    asyncio.create_task(drive_scan_scheduler())


@app.get("/api/health")
def health():
    pol = read_policy()
    return {
        "status": "ok",
        "time": time.time(),
        "panic": PANIC_SWITCH.exists(),
        "policy": pol,
    }


@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.post("/api/admin/refresh_data")
def refresh_data():
    ensure_schema()
    try:
        updated = refresh_from_sheets()
        return {"ok": True, "updated": updated}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@app.post("/api/admin/update_sheets")
def update_sheets(cfg: SheetsConfig):
    cur = read_sheets_config()
    if cfg.revenue_csv_url is not None:
        cur["revenue_csv_url"] = cfg.revenue_csv_url
    if cfg.content_kpis_csv_url is not None:
        cur["content_kpis_csv_url"] = cfg.content_kpis_csv_url
    if cfg.poll_seconds is not None:
        cur["poll_seconds"] = int(cfg.poll_seconds)
    write_sheets_config(cur)
    return {"ok": True, "config": cur}


@app.post("/api/admin/update_sheets_from_sheet")
def update_sheets_from_sheet(data: SheetsFromSheet):
    # Derive CSV export URLs from a view URL
    m = re.search(r"/spreadsheets/d/([a-zA-Z0-9-_]+)", data.sheet_url)
    if not m:
        return {"ok": False, "error": "Invalid Google Sheet URL"}
    sid = m.group(1)

    def csv_for(tab: str) -> str:
        return f"https://docs.google.com/spreadsheets/d/{sid}/gviz/tq?tqx=out:csv&sheet={tab}"

    cfg = read_sheets_config()
    cfg["revenue_csv_url"] = csv_for(data.revenue_tab)
    cfg["content_kpis_csv_url"] = csv_for(data.kpis_tab)
    if data.poll_seconds is not None:
        cfg["poll_seconds"] = int(data.poll_seconds)
    write_sheets_config(cfg)
    return {"ok": True, "config": cfg}


@app.get("/api/admin/last_refresh")
def last_refresh():
    try:
        if LAST_REFRESH_FILE.exists():
            return {"ok": True, "last_refresh": LAST_REFRESH_FILE.read_text().strip()}
        return {"ok": True, "last_refresh": None}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@app.get("/api/admin/panic_status")
def panic_status():
    return {"ok": True, "panic": PANIC_SWITCH.exists()}


@app.post("/api/admin/panic/on")
def panic_on():
    try:
        REPORTS.mkdir(parents=True, exist_ok=True)
        PANIC_SWITCH.write_text("on")
        return {"ok": True, "panic": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@app.post("/api/admin/panic/off")
def panic_off():
    try:
        if PANIC_SWITCH.exists():
            PANIC_SWITCH.unlink()
        return {"ok": True, "panic": False}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@app.get("/api/metrics/revenue")
def revenue_metrics(days: int = 30):
    # Use local computer time to compute cutoff date (inclusive)
    try:
        days = max(1, int(days))
    except Exception:
        days = 30
    today = datetime.now().date()
    cutoff = today - timedelta(days=days - 1)
    cutoff_str = cutoff.strftime("%Y-%m-%d")
    con = db_conn()
    cur = con.cursor()
    cur.execute(
        "select day,goal,actual from revenue_daily where day >= ? order by day asc",
        (cutoff_str,),
    )
    rows = cur.fetchall()
    con.close()
    return JSONResponse([{"day": d, "goal": g, "actual": a} for d, g, a in rows])


@app.get("/api/metrics/content")
def content_metrics():
    con = db_conn()
    cur = con.cursor()
    cur.execute("select metric,value from content_kpis")
    rows = cur.fetchall()
    con.close()
    return JSONResponse({m: v for m, v in rows})


@app.get("/api/plan/first_month")
def first_month_plan():
    return {"plan_markdown": (BASE / "reports" / "FIRST_MONTH_5K_PLAN.md").read_text()}


@app.post("/api/research")
def research(topic: str):
    ART_STAGING.mkdir(parents=True, exist_ok=True)
    p = ART_STAGING / f"seed_{int(time.time())}.json"
    p.write_text(
        json.dumps(
            {"topic": topic, "bullets": [f"Key insight about {topic}"]}, indent=2
        )
    )
    return {"ok": True, "seed_file": str(p)}


@app.post("/api/draft")
def draft(seed_id: int = 1, content: str = "Write 500 words"):
    ART_STAGING.mkdir(parents=True, exist_ok=True)
    p = ART_STAGING / f"draft_{int(time.time())}.txt"
    p.write_text(f"# Draft for seed {seed_id}\n\n{content}\n")
    con = db_conn()
    cur = con.cursor()
    cur.execute("update content_kpis set value=value+1 where metric='videos_total'")
    con.commit()
    con.close()
    return {"ok": True, "draft_file": str(p)}


@app.post("/api/repurpose")
def repurpose():
    drafts = sorted(ART_STAGING.glob("draft_*.txt"))
    if not drafts:
        return {"ok": False, "error": "No drafts"}
    latest = drafts[-1]
    out = ART_STAGING / f"short_{latest.stem.split('_')[-1]}.txt"
    out.write_text(latest.read_text()[:400] + "\n\n# Short form\n")
    con = db_conn()
    cur = con.cursor()
    cur.execute("update content_kpis set value=value+1 where metric='shorts_total'")
    con.commit()
    con.close()
    return {"ok": True, "short_file": str(out)}


@app.get("/api/admin/approve_publish/true")
def approve_true():
    REPORTS.mkdir(parents=True, exist_ok=True)
    APPROVAL.write_text("approved")
    return {"ok": True, "approved": True}


@app.post("/api/publish")
def publish():
    if PANIC_SWITCH.exists():
        return {"ok": False, "error": "Panic switch ON"}
    if not APPROVAL.exists():
        return {"ok": False, "error": "Not approved"}
    moved = []
    ART_PUBLISHED.mkdir(parents=True, exist_ok=True)
    for p in ART_STAGING.glob("*"):
        t = ART_PUBLISHED / p.name
        t.write_bytes(p.read_bytes())
        moved.append(t.name)
    return {"ok": True, "published": moved}


@app.post("/api/actions/full_video")
def action_full_video(channel: str = "right_perspective", topic: str = "auto"):
    # Convenience endpoint for dashboard button
    payload = {"topic": topic}
    return enqueue_job(
        EnqueueJob(type="full_video", channel=channel, payload_json=payload, priority=5)
    )


@app.post("/api/actions/breaking_news")
def action_breaking_news(channel: str = "right_perspective", topic: str = "breaking"):
    payload = {"topic": topic}
    return enqueue_job(
        EnqueueJob(
            type="breaking_news", channel=channel, payload_json=payload, priority=3
        )
    )


@app.post("/api/actions/short")
def action_short(
    channel: str = "right_perspective", topic: str = "quick take", duration: int = 30
):
    payload = {"topic": topic, "duration": str(int(duration))}
    return enqueue_job(
        EnqueueJob(type="short", channel=channel, payload_json=payload, priority=4)
    )


@app.post("/api/actions/bootstrap_channel")
def action_bootstrap_channel(
    channel: Optional[str] = None, body: Optional[BootstrapRequest] = None
):
    """Bootstrap a channel with N videos and M shorts. Accepts query param or JSON body.
    Defaults: 6 videos, 3 shorts. Zero-warnings: validate inputs and report helpful errors.
    """
    try:
        ch = (channel or (body.channel if body else None) or "").strip()
        vids = body.videos if (body and isinstance(body.videos, int)) else 6
        sh = body.shorts if (body and isinstance(body.shorts, int)) else 3
        if not ch:
            return {
                "ok": False,
                "error": "channel is required (query ?channel=... or JSON {channel:})",
            }
        vids = max(0, min(24, vids))
        sh = max(0, min(24, sh))
        results = []
        for i in range(vids):
            r = enqueue_job(
                EnqueueJob(
                    type="full_video",
                    channel=ch,
                    payload_json={"topic": f"bootstrap {i + 1}"},
                    priority=5,
                )
            )
            results.append(r)
        for i in range(sh):
            r = enqueue_job(
                EnqueueJob(
                    type="short",
                    channel=ch,
                    payload_json={
                        "topic": f"bootstrap short {i + 1}",
                        "duration": "30",
                    },
                    priority=4,
                )
            )
            results.append(r)
        return {
            "ok": True,
            "channel": ch,
            "videos": vids,
            "shorts": sh,
            "enqueued": results,
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def _today_str():
    return datetime.now().strftime("%Y-%m-%d")


def _list_channels_for_scheduling():
    """Derive channel names from sheets_multi.json sources (excluding default/voices)."""
    try:
        data = json.loads((BASE / "config" / "sheets_multi.json").read_text())
        srcs = list((data.get("sources") or {}).keys())
        return [s for s in srcs if s not in ("default", "voices")]
    except Exception:
        return []


async def shorts_scheduler_loop():
    """Ensure 3 shorts/day per channel by checking daily_shorts_log and enqueuing as needed."""
    while True:
        try:
            channels = _list_channels_for_scheduling()
            day = _today_str()
            con = db_conn()
            cur = con.cursor()
            for ch in channels:
                cur.execute(
                    "SELECT count FROM daily_shorts_log WHERE channel=? AND day=?",
                    (ch, day),
                )
                row = cur.fetchone()
                count = row[0] if row else 0
                target = 3
                to_add = max(0, target - count)
                for i in range(to_add):
                    enqueue_job(
                        EnqueueJob(
                            type="short",
                            channel=ch,
                            payload_json={"topic": "daily short", "duration": "30"},
                            priority=4,
                        )
                    )
                    count += 1
                if row:
                    cur.execute(
                        "UPDATE daily_shorts_log SET count=? WHERE channel=? AND day=?",
                        (count, ch, day),
                    )
                else:
                    cur.execute(
                        "INSERT INTO daily_shorts_log(channel,day,count) VALUES (?,?,?)",
                        (ch, day, count),
                    )
            con.commit()
            con.close()
        except Exception as e:
            print("shorts scheduler error:", e)
        await asyncio.sleep(300)  # check every 5 minutes


# ------------------------
# Niches computation (top 10 current year + next)
# ------------------------
def _today_date():
    return datetime.now().date()


def _year_pair():
    d = _today_date()
    return d.year, d.year + 1


def _compute_top_niches(channels: list[str], top_n: int = 10) -> list[str]:
    """Example niche computation. In runtime, this blends:
    - Recent performance (CTR, retention, RPM proxies)
    - Market trends (Sheets, research, seasonal)
    - Channel portfolio gaps and overlap minimization
    Here we derive a stable, diverse top list seeded by channel themes.
    """
    seeds = [
        "AI Tools",
        "Election Watch",
        "Gadget Reviews",
        "Health Hacks",
        "Longevity",
        "Clean Energy",
        "Crypto Macro",
        "Robotics",
        "Creator Economy",
        "Personal Finance",
        "Weight Loss Science",
        "Sleep & Recovery",
        "Home Automation",
        "Cybersecurity",
        "AR/VR",
    ]
    # bias by present channels
    prefer = []
    for ch in channels:
        if "right" in ch:
            prefer += ["Election Watch", "Media Takes", "Policy Breakdown"]
        if "future" in ch:
            prefer += ["AI Tools", "Robotics", "AR/VR"]
        if "next_gen" in ch:
            prefer += ["Gadget Reviews", "Cybersecurity", "Creator Economy"]
        if "eco" in ch:
            prefer += ["Clean Energy", "Health Hacks", "Longevity"]
    pool = list(dict.fromkeys(prefer + seeds))
    return pool[: max(1, min(top_n, len(pool)))]


@app.get("/api/niches/top")
def niches_top():
    con = db_conn()
    cur = con.cursor()
    cur.execute(
        "SELECT day, year, next_year, niches_json FROM niches_top ORDER BY day DESC LIMIT 1"
    )
    row = cur.fetchone()
    con.close()
    if not row:
        return {"ok": True, "day": None, "year": None, "next_year": None, "niches": []}
    return {
        "ok": True,
        "day": row[0],
        "year": row[1],
        "next_year": row[2],
        "niches": json.loads(row[3] or "[]"),
    }


@app.post("/api/niches/refresh")
def niches_refresh():
    channels = _list_channels_for_scheduling()
    niches = _compute_top_niches(channels, top_n=10)
    day = _today_date().strftime("%Y-%m-%d")
    y, ny = _year_pair()
    con = db_conn()
    cur = con.cursor()
    # Retry a few times in case another writer holds the DB briefly
    import sqlite3 as _sqlite3
    import time as _time

    for _attempt in range(5):
        try:
            cur.execute(
                "INSERT OR REPLACE INTO niches_top(day,year,next_year,niches_json) VALUES (?,?,?,?)",
                (day, int(y), int(ny), json.dumps(niches)),
            )
            con.commit()
            con.close()
            break
        except Exception as _e:
            msg = str(_e).lower()
            if isinstance(_e, _sqlite3.OperationalError) and "locked" in msg:
                _time.sleep(0.25)
                continue
            con.close()
            raise
    return {"ok": True, "day": day, "year": y, "next_year": ny, "niches": niches}


async def niches_scheduler_loop():
    """Refresh niches daily. Runs every 6 hours and ensures today's row exists."""
    last_day = None
    while True:
        try:
            day = _today_date().strftime("%Y-%m-%d")
            if day != last_day:
                niches_refresh()
                last_day = day
        except Exception as e:
            print("niches scheduler error:", e)
        await asyncio.sleep(21600)  # 6 hours


@app.get("/api/admin/policy")
def get_policy():
    """Expose the governance policy as read-only to the dashboard."""
    try:
        return {"ok": True, "policy": read_policy()}
    except Exception as e:
        return {"ok": False, "error": str(e)}


# ------------------------
# Integrations config + Imports
# ------------------------

def _read_integrations() -> dict:
    try:
        if INTEGRATIONS_YAML.exists():
            data = yaml.safe_load(INTEGRATIONS_YAML.read_text()) or {}
        else:
            data = {}
    except Exception:
        data = {}
    # normalize keys
    data.setdefault("trae_api_token", "")
    data.setdefault("downloads_path", str(Path.home() / "Downloads"))
    data.setdefault("drive_path", "")
    # New: platform API keys for Trae clients
    data.setdefault("openai_api_key", "")
    data.setdefault("google_ai_api_key", "")
    data.setdefault("abacus_api_key", "")
    return data


def _write_integrations(cfg: dict) -> dict:
    safe = {
        "trae_api_token": str(cfg.get("trae_api_token", "")),
        "downloads_path": str(cfg.get("downloads_path", Path.home() / "Downloads")),
        "drive_path": str(cfg.get("drive_path", "")),
        # New: persist platform keys locally (masked on GET elsewhere)
        "openai_api_key": str(cfg.get("openai_api_key", "")),
        "google_ai_api_key": str(cfg.get("google_ai_api_key", "")),
        "abacus_api_key": str(cfg.get("abacus_api_key", "")),
    }
    INTEGRATIONS_YAML.parent.mkdir(parents=True, exist_ok=True)
    INTEGRATIONS_YAML.write_text(yaml.safe_dump(safe, sort_keys=False))
    return safe


def _mask_secret(s: str) -> str:
    s = s or ""
    if len(s) <= 6:
        return "*" * len(s)
    return s[:3] + "*" * (len(s) - 6) + s[-3:]


@app.get("/api/integrations/config")
def integrations_get():
    cfg = _read_integrations()
    masked = dict(cfg)
    if masked.get("trae_api_token"):
        masked["trae_api_token"] = _mask_secret(masked["trae_api_token"])  # do not leak
    if masked.get("openai_api_key"):
        masked["openai_api_key"] = _mask_secret(masked["openai_api_key"])  # do not leak
    if masked.get("google_ai_api_key"):
        masked["google_ai_api_key"] = _mask_secret(masked["google_ai_api_key"])  # do not leak
    if masked.get("abacus_api_key"):
        masked["abacus_api_key"] = _mask_secret(masked["abacus_api_key"])  # do not leak
    return {"ok": True, "config": masked}


class IntegrationsUpdate(BaseModel):
    trae_api_token: Optional[str] = None
    downloads_path: Optional[str] = None
    drive_path: Optional[str] = None
    # New: platform keys for Trae.ai clients (kept locally, masked on GET)
    openai_api_key: Optional[str] = None
    google_ai_api_key: Optional[str] = None
    abacus_api_key: Optional[str] = None


@app.post("/api/integrations/config")
def integrations_post(data: IntegrationsUpdate):
    cur = _read_integrations()
    if data.trae_api_token is not None:
        cur["trae_api_token"] = data.trae_api_token.strip()
    if data.downloads_path is not None:
        cur["downloads_path"] = data.downloads_path.strip() or str(Path.home() / "Downloads")
    if data.drive_path is not None:
        cur["drive_path"] = data.drive_path.strip()
    # New: platform keys
    if getattr(data, "openai_api_key", None) is not None:
        cur["openai_api_key"] = (data.openai_api_key or "").strip()
    if getattr(data, "google_ai_api_key", None) is not None:
        cur["google_ai_api_key"] = (data.google_ai_api_key or "").strip()
    if getattr(data, "abacus_api_key", None) is not None:
        cur["abacus_api_key"] = (data.abacus_api_key or "").strip()
    saved = _write_integrations(cur)
    masked = dict(saved)
    if masked.get("trae_api_token"):
        masked["trae_api_token"] = _mask_secret(masked["trae_api_token"])  # mask in response
    if masked.get("openai_api_key"):
        masked["openai_api_key"] = _mask_secret(masked["openai_api_key"])  # mask in response
    if masked.get("google_ai_api_key"):
        masked["google_ai_api_key"] = _mask_secret(masked["google_ai_api_key"])  # mask in response
    if masked.get("abacus_api_key"):
        masked["abacus_api_key"] = _mask_secret(masked["abacus_api_key"])  # mask in response
    return {"ok": True, "config": masked}


def _safe_under(root: Path, p: Path) -> bool:
    try:
        return str(p.resolve()).startswith(str(root.resolve()) + "/") or p.resolve() == root.resolve()
    except Exception:
        return False


@app.get("/api/imports/list")
def imports_list(source: str = "downloads", glob: str = "**/*"):
    cfg = _read_integrations()
    if source not in ("downloads", "drive"):
        return {"ok": False, "error": "invalid source"}
    root = Path(cfg["downloads_path"]) if source == "downloads" else Path(cfg.get("drive_path") or "")
    if not root.exists():
        return {"ok": False, "error": f"root not found: {root}"}
    # Restrict listing to a reasonable size
    try:
        paths = []
        for i, p in enumerate(sorted(root.glob(glob))):
            if i >= 500:
                break
            if p.is_file():
                rel = str(p.relative_to(root))
                st = p.stat()
                paths.append({"rel": rel, "size": st.st_size})
        return {"ok": True, "root": str(root), "count": len(paths), "items": paths}
    except Exception as e:
        return {"ok": False, "error": str(e)}


class IngestRequest(BaseModel):
    source: str
    items: List[str]  # relative paths under the source root


@app.post("/api/imports/ingest")
def imports_ingest(req: IngestRequest):
    cfg = _read_integrations()
    if req.source not in ("downloads", "drive"):
        return {"ok": False, "error": "invalid source"}
    root = Path(cfg["downloads_path"]) if req.source == "downloads" else Path(cfg.get("drive_path") or "")
    if not root.exists():
        return {"ok": False, "error": f"root not found: {root}"}
    ART_STAGING.mkdir(parents=True, exist_ok=True)
    copied = []
    for rel in req.items or []:
        try:
            src = (root / rel).resolve()
            if not _safe_under(root, src) or not src.is_file():
                continue
            dest = ART_STAGING / (src.name)
            # If name collision, add a suffix timestamp
            if dest.exists():
                dest = ART_STAGING / f"{int(time.time())}_{src.name}"
            dest.write_bytes(src.read_bytes())
            copied.append(dest.name)
        except Exception:
            continue
    return {"ok": True, "copied": copied, "staging": str(ART_STAGING)}

# ------------------------
# Web Guard integration
# ------------------------

def _launchctl_loaded() -> bool:
    try:
        out = subprocess.run(["launchctl", "list"], capture_output=True, text=True)
        return "com.monkeypaw.webguard" in (out.stdout or "")
    except Exception:
        return False


def _read_guard_cfg() -> dict:
    try:
        if RUNTIME_YML.exists():
            return yaml.safe_load(RUNTIME_YML.read_text()) or {}
    except Exception:
        pass
    return {}


def _log_tail(n: int = 80) -> list[str]:
    try:
        if not GUARD_LOG.exists():
            return []
        # Efficient tail read
        with GUARD_LOG.open("rb") as f:
            try:
                f.seek(0, os.SEEK_END)
                size = f.tell()
                block = 1024
                data = b""
                while size > 0 and data.count(b"\n") <= n:
                    step = min(block, size)
                    size -= step
                    f.seek(size)
                    data = f.read(step) + data
                lines = data.splitlines()[-n:]
                return [ln.decode("utf-8", "replace") for ln in lines]
            except Exception:
                return GUARD_LOG.read_text(errors="replace").splitlines()[-n:]
    except Exception:
        return []


@app.get("/api/guard/status")
def guard_status():
    cfg = _read_guard_cfg()
    return {
        "ok": True,
        "present": PACK_DIR.exists(),
        "venv_python": str(PACK_VENV_PY),
        "venv_python_exists": PACK_VENV_PY.exists(),
        "script": str(GUARD_SCRIPT),
        "script_exists": GUARD_SCRIPT.exists(),
        "log": str(GUARD_LOG),
        "log_exists": GUARD_LOG.exists(),
        "launch_agent": str(LAUNCH_AGENT),
        "launch_agent_exists": LAUNCH_AGENT.exists(),
        "launchctl_loaded": _launchctl_loaded(),
        "config": cfg,
    }


@app.post("/api/guard/dry_run_once")
def guard_dry_run_once(timeout_sec: int = 5):
    if not (PACK_VENV_PY.exists() and GUARD_SCRIPT.exists()):
        return {"ok": False, "error": "guard not installed"}
    try:
        cp = subprocess.run(
            [str(PACK_VENV_PY), str(GUARD_SCRIPT), "--dry-run", "--once"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=max(1, min(30, int(timeout_sec or 5))),
        )
        out = (cp.stdout or "").splitlines()[-40:]
        return {"ok": True, "rc": cp.returncode, "stdout_tail": out, "log_tail": _log_tail(60)}
    except subprocess.TimeoutExpired as e:
        return {"ok": False, "error": "timeout", "partial": (e.stdout or "").splitlines()[-40:]}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@app.get("/api/guard/log_tail")
def guard_log_tail(lines: int = 80):
    try:
        n = max(1, min(500, int(lines)))
    except Exception:
        n = 80
    return {"ok": True, "lines": _log_tail(n)}


# ------------------------
# Resources (prompts + registry) from installed pack
# ------------------------

DUAL_PROMPT = PACK_DIR / "prompts" / "dual_engine_prompt.md"
UNI_ACCESS = PACK_DIR / "prompts" / "university_access.md"
REGISTRY_JSON = PACK_DIR / "registry" / "nocode_coders_registry.json"


@app.get("/api/resources/dual_engine_prompt")
def resources_dual_engine_prompt():
    try:
        if DUAL_PROMPT.exists():
            return {"ok": True, "markdown": DUAL_PROMPT.read_text(errors="replace")}
        return {"ok": False, "error": f"not found: {DUAL_PROMPT}"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@app.get("/api/resources/university_access")
def resources_university_access():
    try:
        if UNI_ACCESS.exists():
            return {"ok": True, "markdown": UNI_ACCESS.read_text(errors="replace")}
        return {"ok": False, "error": f"not found: {UNI_ACCESS}"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@app.get("/api/resources/registry")
def resources_registry(full: int = 0):
    try:
        p = REGISTRY_JSON if REGISTRY_JSON.exists() else (Path.home() / "Desktop" / "monkey-paw" / "nocode_coders_registry.json")
        if not p.exists():
            return {"ok": False, "error": f"registry not found at {p}"}
        data = json.loads(p.read_text(errors="replace") or "[]")
        if int(full or 0):
            return {"ok": True, "count": len(data), "items": data}
        # summary by category
        cats = {}
        free = 0
        for item in data:
            cats[item.get("category","uncategorized")] = cats.get(item.get("category","uncategorized"), 0) + 1
            if item.get("free_plan"):
                free += 1
        return {"ok": True, "count": len(data), "free_plan": free, "by_category": cats}
    except Exception as e:
        return {"ok": False, "error": str(e)}

# ------------------------
# Jobs API and worker impl
# ------------------------


def job_event(cur, job_id: int, level: str, message: str, data: Optional[dict] = None):
    cur.execute(
        "INSERT INTO job_events(job_id, ts, level, message, data_json) VALUES (?,?,?,?,?)",
        (job_id, time.time(), level, message, json.dumps(data or {})),
    )


@app.post("/api/jobs/enqueue")
def enqueue_job(j: EnqueueJob):
    con = db_conn()
    cur = con.cursor()
    now = time.time()
    cur.execute(
        """
        INSERT INTO jobs(type, channel, payload_json, status, priority, retries, next_run_at, created_at, updated_at)
        VALUES (?,?,?,?,?,?,?, ?, ?)
        """,
        (
            j.type,
            j.channel or "default",
            json.dumps(j.payload_json or {}),
            "queued",
            int(j.priority or 5),
            0,
            now,
            now,
            now,
        ),
    )
    job_id = cur.lastrowid
    job_event(
        cur,
        job_id,
        "info",
        "enqueued",
        {"type": j.type, "channel": j.channel or "default"},
    )
    con.commit()
    con.close()
    return {"ok": True, "job_id": job_id}


@app.get("/api/jobs/recent")
def jobs_recent(limit: int = 25):
    con = db_conn()
    cur = con.cursor()
    cur.execute(
        "SELECT id, type, channel, status, priority, retries, created_at, updated_at FROM jobs ORDER BY id DESC LIMIT ?",
        (max(1, min(200, limit)),),
    )
    rows = [
        {
            "id": i,
            "type": t,
            "channel": c,
            "status": s,
            "priority": p,
            "retries": r,
            "created_at": ca,
            "updated_at": ua,
        }
        for i, t, c, s, p, r, ca, ua in cur.fetchall()
    ]
    con.close()
    return {"ok": True, "jobs": rows}


@app.get("/api/jobs/{job_id}")
def job_detail(job_id: int):
    con = db_conn()
    cur = con.cursor()
    cur.execute(
        "SELECT id, type, channel, payload_json, status, priority, retries, created_at, updated_at FROM jobs WHERE id=?",
        (job_id,),
    )
    row = cur.fetchone()
    if not row:
        con.close()
        return {"ok": False, "error": "job not found"}
    job = {
        "id": row[0],
        "type": row[1],
        "channel": row[2],
        "payload_json": json.loads(row[3] or "{}"),
        "status": row[4],
        "priority": row[5],
        "retries": row[6],
        "created_at": row[7],
        "updated_at": row[8],
    }
    cur.execute(
        "SELECT ts, level, message, data_json FROM job_events WHERE job_id=? ORDER BY id ASC",
        (job_id,),
    )
    ev = [
        {"ts": ts, "level": lvl, "message": msg, "data": json.loads(d or "{}")}
        for ts, lvl, msg, d in cur.fetchall()
    ]
    con.close()
    return {"ok": True, "job": job, "events": ev}


def process_one_job() -> bool:
    con = db_conn()
    cur = con.cursor()
    now = time.time()
    cur.execute(
        "SELECT id, type, channel, payload_json, retries FROM jobs WHERE status IN ('queued','retry') AND (next_run_at IS NULL OR next_run_at <= ?) ORDER BY priority ASC, id ASC LIMIT 1",
        (now,),
    )
    row = cur.fetchone()
    if not row:
        con.close()
        return False
    job_id, jtype, channel, payload_json, retries = row
    payload = json.loads(payload_json or "{}")
    cur.execute(
        "UPDATE jobs SET status='running', updated_at=? WHERE id=?", (now, job_id)
    )
    job_event(cur, job_id, "info", "started", {"type": jtype, "channel": channel})
    con.commit()

    try:
        # Demo pipelines (extend later):
        if jtype == "full_video":
            run_full_video_pipeline(cur, job_id, channel, payload)
        elif jtype == "breaking_news":
            run_breaking_news_pipeline(cur, job_id, channel, payload)
        elif jtype == "short":
            run_short_pipeline(cur, job_id, channel, payload)
        else:
            job_event(cur, job_id, "warning", "unknown job type", {"type": jtype})

        cur.execute(
            "UPDATE jobs SET status='done', updated_at=? WHERE id=?",
            (time.time(), job_id),
        )
        job_event(cur, job_id, "info", "completed")
        con.commit()
        con.close()
        return True
    except Exception as e:
        retries = int(retries or 0) + 1
        delay = min(180, 2 ** min(6, retries))
        nxt = time.time() + delay
        job_event(
            cur,
            job_id,
            "error",
            "failed",
            {"error": str(e), "retries": retries, "next_delay_sec": delay},
        )
        cur.execute(
            "UPDATE jobs SET status='retry', retries=?, next_run_at=?, updated_at=? WHERE id=?",
            (retries, nxt, time.time(), job_id),
        )
        con.commit()
        con.close()
        return True


def run_full_video_pipeline(cur, job_id: int, channel: str, payload: dict):
    # Example steps with file outputs to artifacts/staging
    ART_STAGING.mkdir(parents=True, exist_ok=True)
    ts = int(time.time())
    script = ART_STAGING / f"script_{channel}_{ts}.txt"
    voice = ART_STAGING / f"voice_{channel}_{ts}.wav"
    video = ART_STAGING / f"video_{channel}_{ts}.mp4"
    thumb = ART_STAGING / f"thumb_{channel}_{ts}.png"

    job_event(cur, job_id, "info", "research")
    (ART_STAGING / f"seed_{ts}.json").write_text(
        json.dumps(
            {"channel": channel, "topic": payload.get("topic", "auto")}, indent=2
        )
    )
    job_event(cur, job_id, "info", "script")
    script.write_text(f"# Script for {channel}\n\nHook...\nBody...\nCTA...\n")
    # TTS via macOS 'say' if available, else fallback silent wav
    job_event(cur, job_id, "info", "tts")
    try:
        text = f"This is an auto-generated narration for {channel}. Example script."
        say_bin = shutil.which("say")
        if say_bin:
            aiff_tmp = ART_STAGING / f"voice_{channel}_{ts}.aiff"
            subprocess.run([say_bin, text, "-o", str(aiff_tmp)], check=True)
            # Convert to wav via ffmpeg if available
            ffmpeg_bin = shutil.which("ffmpeg")
            if ffmpeg_bin:
                subprocess.run(
                    [ffmpeg_bin, "-y", "-i", str(aiff_tmp), str(voice)], check=True
                )
                try:
                    aiff_tmp.unlink(missing_ok=True)
                except Exception:
                    pass
            else:
                # If no ffmpeg, keep aiff as voice
                voice = aiff_tmp
        else:
            # Fallback silent wav (1s)
            ffmpeg_bin = shutil.which("ffmpeg")
            if ffmpeg_bin:
                subprocess.run(
                    [
                        ffmpeg_bin,
                        "-y",
                        "-f",
                        "lavfi",
                        "-i",
                        "anullsrc=r=44100:cl=mono",
                        "-t",
                        "1",
                        str(voice),
                    ],
                    check=True,
                )
            else:
                voice.write_bytes(b"RIFF0000WAVE")
    except Exception as e:
        job_event(cur, job_id, "warning", "tts_fallback", {"error": str(e)})
        try:
            voice.write_bytes(b"RIFF0000WAVE")
        except Exception:
            pass

    # QA triple-checks: ensure outputs exist and are non-empty
    try:

        def _ok(p: Path) -> bool:
            try:
                return p.exists() and p.stat().st_size > 0
            except Exception:
                return False

        checks = {
            "script": _ok(script),
            "voice": _ok(voice),
            "video": _ok(video),
            "thumb": _ok(thumb),
        }
        job_event(cur, job_id, "info", "qa_checks", {"checks": checks})
        if not all(checks.values()):
            missing = [k for k, v in checks.items() if not v]
            raise RuntimeError(f"QA failed: missing or empty {missing}")
    except Exception as e:
        job_event(cur, job_id, "warning", "qa_failed", {"error": str(e)})

    # Assemble simple video via ffmpeg: solid background + optional logo overlay + voice audio
    # Prefer Apple Silicon hardware encoder (h264_videotoolbox) on M1 for speed/quality
    job_event(cur, job_id, "info", "assemble")
    try:
        ffmpeg_bin = shutil.which("ffmpeg")
        if ffmpeg_bin:
            # Determine duration target (default 15s)
            duration = "15"
            # Build background color and size
            size = "1920x1080"
            bg = "color=c=black:s=" + size + ":d=" + duration
            # Optional logo overlay if exists
            logo = None
            for p in [
                BASE / "assets" / "Overlays" / "logo.png",
                BASE / "assets" / "Overlays" / "logo.jpg",
                BASE / "assets" / "Overlays" / "logo.jpeg",
            ]:
                if p.exists():
                    logo = p
                    break
            # encoder preference order
            encoders = ["h264_videotoolbox", "libx264"]
            chosen = None
            if logo:
                # background -> overlay logo (top-right) -> add audio
                last_err = None
                for enc in encoders:
                    try:
                        subprocess.run(
                            [
                                ffmpeg_bin,
                                "-y",
                                "-f",
                                "lavfi",
                                "-i",
                                bg,
                                "-i",
                                str(logo),
                                "-filter_complex",
                                "[0:v][1:v]overlay=W-w-50:50,format=yuv420p",
                                "-i",
                                str(voice),
                                "-shortest",
                                "-c:v",
                                enc,
                                "-pix_fmt",
                                "yuv420p",
                                "-c:a",
                                "aac",
                                "-b:a",
                                "192k",
                                str(video),
                            ],
                            check=True,
                        )
                        chosen = enc
                        break
                    except Exception as e:
                        last_err = e
                        continue
                if not chosen:
                    raise last_err or RuntimeError("No encoder succeeded")
            else:
                last_err = None
                for enc in encoders:
                    try:
                        subprocess.run(
                            [
                                ffmpeg_bin,
                                "-y",
                                "-f",
                                "lavfi",
                                "-i",
                                bg,
                                "-i",
                                str(voice),
                                "-shortest",
                                "-c:v",
                                enc,
                                "-pix_fmt",
                                "yuv420p",
                                "-c:a",
                                "aac",
                                "-b:a",
                                "192k",
                                str(video),
                            ],
                            check=True,
                        )
                        chosen = enc
                        break
                    except Exception as e:
                        last_err = e
                        continue
                if not chosen:
                    raise last_err or RuntimeError("No encoder succeeded")
            job_event(cur, job_id, "info", "assemble_encoder", {"encoder": chosen})
        else:
            video.write_bytes(b"\x00\x00substitute_mp4")
    except Exception as e:
        job_event(cur, job_id, "warning", "assemble_fallback", {"error": str(e)})
        try:
            video.write_bytes(b"\x00\x00substitute_mp4")
        except Exception:
            pass

    # Generate thumbnail via ffmpeg drawtext if possible; fallback to simple bytes
    job_event(cur, job_id, "info", "thumbnail")
    try:
        ffmpeg_bin = shutil.which("ffmpeg")
        if ffmpeg_bin:
            # Pick a font if available
            font = None
            fonts_dir = BASE / "assets" / "Fonts"
            if fonts_dir.exists():
                for f in fonts_dir.glob("*.ttf"):
                    font = f
                    break
                if not font:
                    for f in fonts_dir.glob("*.otf"):
                        font = f
                        break
            text = f"{channel}"[:40]
            draw = f"drawtext=fontfile='{font if font else '/System/Library/Fonts/Supplemental/Arial Unicode.ttf'}':text='{text}':fontsize=72:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2"
            subprocess.run(
                [
                    ffmpeg_bin,
                    "-y",
                    "-f",
                    "lavfi",
                    "-i",
                    "color=c=0x222233:s=1280x720:d=1",
                    "-vframes",
                    "1",
                    "-vf",
                    draw,
                    str(thumb),
                ],
                check=True,
            )
        else:
            thumb.write_bytes(b"PNG")
    except Exception as e:
        job_event(cur, job_id, "warning", "thumbnail_fallback", {"error": str(e)})
        try:
            thumb.write_bytes(b"PNG")
        except Exception:
            pass


def run_breaking_news_pipeline(cur, job_id: int, channel: str, payload: dict):
    ART_STAGING.mkdir(parents=True, exist_ok=True)
    ts = int(time.time())
    note = ART_STAGING / f"breaking_{channel}_{ts}.txt"
    job_event(cur, job_id, "info", "breaking_note")
    note.write_text(f"Breaking for {channel}: {payload.get('topic', 'auto')}\n")


def run_short_pipeline(cur, job_id: int, channel: str, payload: dict):
    """Create a vertical short (1080x1920) with quick text and optional bg.
    This is a lightweight pipeline so we can produce 3/day per channel reliably.
    """
    ART_STAGING.mkdir(parents=True, exist_ok=True)
    ts = int(time.time())
    script = ART_STAGING / f"short_script_{channel}_{ts}.txt"
    voice = ART_STAGING / f"short_voice_{channel}_{ts}.wav"
    video = ART_STAGING / f"short_video_{channel}_{ts}.mp4"
    try:
        topic = payload.get("topic", "short update")
        # Script
        script.write_text(f"# Short Script for {channel}\n\n{topic}: Quick take.\n")
        # TTS via say
        say_bin = shutil.which("say")
        ffmpeg_bin = shutil.which("ffmpeg")
        if say_bin:
            aiff_tmp = ART_STAGING / f"short_voice_{channel}_{ts}.aiff"
            subprocess.run(
                [say_bin, f"Quick update: {topic}", "-o", str(aiff_tmp)], check=True
            )
            if ffmpeg_bin:
                subprocess.run(
                    [ffmpeg_bin, "-y", "-i", str(aiff_tmp), str(voice)], check=True
                )
                try:
                    aiff_tmp.unlink(missing_ok=True)
                except Exception:
                    pass
            else:
                voice = aiff_tmp
        else:
            if ffmpeg_bin:
                subprocess.run(
                    [
                        ffmpeg_bin,
                        "-y",
                        "-f",
                        "lavfi",
                        "-i",
                        "anullsrc=r=44100:cl=mono",
                        "-t",
                        "1",
                        str(voice),
                    ],
                    check=True,
                )
            else:
                voice.write_bytes(b"RIFF0000WAVE")
        # Video vertical 1080x1920
        if ffmpeg_bin:
            size = "1080x1920"
            duration = payload.get("duration", "30")
            bg = f"color=c=black:s={size}:d={duration}"
            # Prefer Apple Silicon encoder if available
            encoders = ["h264_videotoolbox", "libx264"]
            last_err = None
            chosen = None
            for enc in encoders:
                try:
                    subprocess.run(
                        [
                            ffmpeg_bin,
                            "-y",
                            "-f",
                            "lavfi",
                            "-i",
                            bg,
                            "-i",
                            str(voice),
                            "-shortest",
                            "-c:v",
                            enc,
                            "-pix_fmt",
                            "yuv420p",
                            "-c:a",
                            "aac",
                            "-b:a",
                            "160k",
                            str(video),
                        ],
                        check=True,
                    )
                    chosen = enc
                    break
                except Exception as e:
                    last_err = e
                    continue
            if not chosen:
                raise last_err or RuntimeError("No encoder succeeded")
            job_event(cur, job_id, "info", "short_encoder", {"encoder": chosen})
        else:
            video.write_bytes(b"\x00\x00substitute_mp4")
    except Exception as e:
        job_event(cur, job_id, "error", "short_failed", {"error": str(e)})
        raise
