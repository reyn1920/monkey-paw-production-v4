from fastapi import FastAPI, Request, Body
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from pydantic import BaseModel
import sqlite3, time, json

BASE = Path(__file__).resolve().parents[1]
DB_MAIN = BASE / "db" / "monkey_paw.db"
REPORTS = BASE / "reports"
PANIC_SWITCH = REPORTS / "PANIC_SWITCH.true"
APPROVAL_FLAG = REPORTS / "approve_publish.true"
ART_STAGING = BASE / "artifacts" / "staging"
ART_PUBLISHED = BASE / "artifacts" / "published"

templates = Jinja2Templates(directory=str(BASE / "app" / "templates"))

app = FastAPI(title="Monkey Paw — All-In-One", version="1.0.0")
app.mount("/static", StaticFiles(directory=str(BASE / "app" / "static")), name="static")

def db_conn():
    return sqlite3.connect(str(DB_MAIN))

@app.get("/api/health")
def health():
    return {"status": "ok", "time": time.time(), "panic": PANIC_SWITCH.exists()}

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

# --- Metrics APIs ---
@app.get("/api/metrics/revenue")
def revenue_metrics():
    con = db_conn(); cur = con.cursor()
    cur.execute("select day, goal, actual from revenue_daily order by day asc")
    rows = cur.fetchall(); con.close()
    return JSONResponse([{"day": d, "goal": g, "actual": a} for d,g,a in rows])

@app.get("/api/metrics/content")
def content_metrics():
    con = db_conn(); cur = con.cursor()
    cur.execute("select metric, value from content_kpis")
    rows = cur.fetchall(); con.close()
    return JSONResponse({m:v for m,v in rows})

@app.get("/api/plan/first_month")
def first_month_plan():
    plan = (BASE / "reports" / "FIRST_MONTH_5K_PLAN.md").read_text()
    return {"plan_markdown": plan}

# --- Pipeline DTOs ---
class ResearchIn(BaseModel):
    topic: str

class DraftIn(BaseModel):
    seed_id: int = 1
    content: str

# --- Pipeline endpoints ---
@app.post("/api/research")
def research(payload: ResearchIn):
    ART_STAGING.mkdir(parents=True, exist_ok=True)
    seed_path = ART_STAGING / f"seed_{int(time.time())}.json"
    seed = {"topic": payload.topic, "bullets": [f"Key insight about {payload.topic}", "Audience: general", "Tone: clear"]}
    seed_path.write_text(json.dumps(seed, indent=2))
    return {"ok": True, "seed_file": str(seed_path)}

@app.post("/api/draft")
def draft(payload: DraftIn):
    ART_STAGING.mkdir(parents=True, exist_ok=True)
    fname = ART_STAGING / f"draft_{int(time.time())}.txt"
    text = f"# Draft for seed {payload.seed_id}\n\n{payload.content}\n\n— Monkey Paw pipeline\n"
    fname.write_text(text)
    # increment KPI
    con = db_conn(); cur = con.cursor()
    cur.execute("update content_kpis set value=value+1 where metric='videos_total'")
    con.commit(); con.close()
    return {"ok": True, "draft_file": str(fname)}

@app.post("/api/repurpose")
def repurpose(seed_id: int = 1):
    drafts = sorted(ART_STAGING.glob("draft_*.txt"))
    if not drafts:
        return {"ok": False, "error": "No drafts available"}
    latest = drafts[-1]
    short = ART_STAGING / f"short_{latest.stem.split('_')[-1]}.txt"
    short.write_text(latest.read_text()[:400] + "\n\n# Short form\n")
    con = db_conn(); cur = con.cursor()
    cur.execute("update content_kpis set value=value+1 where metric='shorts_total'")
    con.commit(); con.close()
    return {"ok": True, "short_file": str(short), "from": latest.name}

@app.post("/api/publish")
def publish():
    if PANIC_SWITCH.exists():
        return {"ok": False, "error": "Panic switch ON. Publishing blocked."}
    if not APPROVAL_FLAG.exists():
        return {"ok": False, "error": "Not approved. Call /api/admin/approve_publish/true first."}
    moved = []
    for p in ART_STAGING.glob("*"):
        target = ART_PUBLISHED / p.name
        target.write_bytes(p.read_bytes())
        moved.append(target.name)
    return {"ok": True, "published": moved}

@app.get("/api/admin/approve_publish/{flag}")
def approve(flag: str):
    if flag.lower() == "true":
        REPORTS.mkdir(parents=True, exist_ok=True)
        APPROVAL_FLAG.write_text("approved")
        return {"ok": True, "approved": True}
    if APPROVAL_FLAG.exists():
        APPROVAL_FLAG.unlink()
    return {"ok": True, "approved": False}
