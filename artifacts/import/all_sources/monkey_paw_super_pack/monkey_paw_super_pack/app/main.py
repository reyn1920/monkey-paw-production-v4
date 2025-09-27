from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import sqlite3, time, json

BASE = Path(__file__).resolve().parents[1]
DB = BASE / "db" / "monkey_paw.db"
ART = BASE / "artifacts"
templates = Jinja2Templates(directory=str(BASE / "app" / "templates"))

app = FastAPI(title="Monkey Paw — Super Pack", version="1.0.0")
app.mount("/static", StaticFiles(directory=str(BASE / "app" / "static")), name="static")

def db_conn():
    return sqlite3.connect(str(DB))

@app.get("/api/health")
def health():
    return {"status":"ok","time": time.time()}

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

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
