from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import sqlite3, time, json

BASE = Path(__file__).resolve().parents[1]
DB_MAIN = BASE / "db" / "monkey_paw.db"
REPORTS = BASE / "reports"
PANIC_SWITCH = REPORTS / "PANIC_SWITCH.true"
APPROVAL = REPORTS / "approve_publish.true"
ART_STAGING = BASE / "artifacts" / "staging"
ART_PUBLISHED = BASE / "artifacts" / "published"

templates = Jinja2Templates(directory=str(BASE / "app" / "templates"))
app = FastAPI(title="Monkey Paw — V4", version="4.0.0")
app.mount("/static", StaticFiles(directory=str(BASE / "app" / "static")), name="static")

def db_conn(): return sqlite3.connect(str(DB_MAIN))

@app.get("/api/health")
def health(): return {"status":"ok","time":time.time(),"panic":PANIC_SWITCH.exists()}

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/api/metrics/revenue")
def revenue_metrics():
    con=db_conn(); cur=con.cursor()
    cur.execute("select day,goal,actual from revenue_daily order by day asc")
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
