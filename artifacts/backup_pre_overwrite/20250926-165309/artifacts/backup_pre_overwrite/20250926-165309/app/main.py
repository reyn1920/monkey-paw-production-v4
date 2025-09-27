from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import sqlite3, time, json
import asyncio, csv, io
from datetime import datetime, timedelta
from typing import Optional
import yaml, requests
from pydantic import BaseModel
import re
from fastapi.middleware.cors import CORSMiddleware

BASE = Path(__file__).resolve().parents[1]
DB_MAIN = BASE / "db" / "monkey_paw.db"
REPORTS = BASE / "reports"
PANIC_SWITCH = REPORTS / "PANIC_SWITCH.true"
APPROVAL = REPORTS / "approve_publish.true"
ART_STAGING = BASE / "artifacts" / "staging"
ART_PUBLISHED = BASE / "artifacts" / "published"
SHEETS_CONFIG = BASE / "config" / "sheets.yaml"
LAST_REFRESH_FILE = BASE / "out" / "last_refresh.txt"

templates = Jinja2Templates(directory=str(BASE / "app" / "templates"))
app = FastAPI(title="Monkey Paw — V4", version="4.0.0")
app.mount("/static", StaticFiles(directory=str(BASE / "app" / "static")), name="static")
from .routers import sheets_router
app.include_router(sheets_router.router)

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

def db_conn(): return sqlite3.connect(str(DB_MAIN))

def ensure_schema():
    con = db_conn(); cur = con.cursor()
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
    con.commit(); con.close()

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

def refresh_from_sheets():
    cfg = read_sheets_config()
    rev_url = (cfg.get("revenue_csv_url") or "").strip()
    kpi_url = (cfg.get("content_kpis_csv_url") or "").strip()
    updated = {"revenue": 0, "kpis": 0}

    if not (rev_url or kpi_url):
        return {"skipped": True, **updated}

    con = db_conn(); cur = con.cursor()
    # Revenue
    if rev_url:
        r = requests.get(rev_url, timeout=15); r.raise_for_status()
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
                g = 0.0; a = 0.0
            cur.execute("INSERT OR REPLACE INTO revenue_daily(day,goal,actual) VALUES (?,?,?)", (str(day), g, a))
            updated["revenue"] += 1

    # KPIs
    if kpi_url:
        r = requests.get(kpi_url, timeout=15); r.raise_for_status()
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
            cur.execute("INSERT OR REPLACE INTO content_kpis(metric,value) VALUES (?,?)", (str(metric), v))
            updated["kpis"] += 1

    con.commit(); con.close()
    # write last refresh timestamp (local time)
    try:
        LAST_REFRESH_FILE.parent.mkdir(parents=True, exist_ok=True)
        LAST_REFRESH_FILE.write_text(datetime.now().isoformat())
    except Exception:
        pass
    return updated

class SheetsConfig(BaseModel):
    revenue_csv_url: Optional[str] = None
    content_kpis_csv_url: Optional[str] = None
    poll_seconds: Optional[int] = None

class SheetsFromSheet(BaseModel):
    sheet_url: str
    revenue_tab: str = "revenue_daily"
    kpis_tab: str = "content_kpis"
    poll_seconds: Optional[int] = None

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

@app.get("/api/health")
def health(): return {"status":"ok","time":time.time(),"panic":PANIC_SWITCH.exists()}

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
    cutoff = today - timedelta(days=days-1)
    cutoff_str = cutoff.strftime('%Y-%m-%d')
    con=db_conn(); cur=con.cursor()
    cur.execute("select day,goal,actual from revenue_daily where day >= ? order by day asc", (cutoff_str,))
    rows=cur.fetchall(); con.close()
    return JSONResponse([{"day":d,"goal":g,"actual":a} for d,g,a in rows])

@app.get("/api/metrics/content")
def content_metrics():
    con=db_conn(); cur=con.cursor()
    cur.execute("select metric,value from content_kpis")
    rows=cur.fetchall(); con.close()
    return JSONResponse({m:v for m,v in rows})

@app.get("/api/plan/first_month")
def first_month_plan():
    return {"plan_markdown": (BASE/"reports"/"FIRST_MONTH_5K_PLAN.md").read_text()}

@app.post("/api/research")
def research(topic: str):
    ART_STAGING.mkdir(parents=True, exist_ok=True)
    p = ART_STAGING / f"seed_{int(time.time())}.json"
    p.write_text(json.dumps({"topic":topic,"bullets":[f"Key insight about {topic}"]}, indent=2))
    return {"ok":True,"seed_file":str(p)}

@app.post("/api/draft")
def draft(seed_id: int=1, content: str="Write 500 words"):
    ART_STAGING.mkdir(parents=True, exist_ok=True)
    p = ART_STAGING / f"draft_{int(time.time())}.txt"
    p.write_text(f"# Draft for seed {seed_id}\n\n{content}\n")
    con=db_conn(); cur=con.cursor(); cur.execute("update content_kpis set value=value+1 where metric='videos_total'"); con.commit(); con.close()
    return {"ok":True,"draft_file":str(p)}

@app.post("/api/repurpose")
def repurpose():
    drafts=sorted(ART_STAGING.glob("draft_*.txt"))
    if not drafts: return {"ok":False,"error":"No drafts"}
    latest=drafts[-1]; out=ART_STAGING/f"short_{latest.stem.split('_')[-1]}.txt"
    out.write_text(latest.read_text()[:400]+"\n\n# Short form\n")
    con=db_conn(); cur=con.cursor(); cur.execute("update content_kpis set value=value+1 where metric='shorts_total'"); con.commit(); con.close()
    return {"ok":True,"short_file":str(out)}

@app.get("/api/admin/approve_publish/true")
def approve_true():
    REPORTS.mkdir(parents=True, exist_ok=True); APPROVAL.write_text("approved"); return {"ok":True,"approved":True}

@app.post("/api/publish")
def publish():
    if PANIC_SWITCH.exists(): return {"ok":False,"error":"Panic switch ON"}
    if not APPROVAL.exists(): return {"ok":False,"error":"Not approved"}
    moved=[]; ART_PUBLISHED.mkdir(parents=True, exist_ok=True)
    for p in ART_STAGING.glob("*"):
        t=ART_PUBLISHED/p.name; t.write_bytes(p.read_bytes()); moved.append(t.name)
    return {"ok":True,"published":moved}
