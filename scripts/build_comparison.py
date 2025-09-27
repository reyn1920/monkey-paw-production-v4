#!/usr/bin/env python3
import os, json, pathlib, re, datetime

ROOT = pathlib.Path(".").resolve()
REPORTS = ROOT / "reports"
out_dir = REPORTS
baseline_path = pathlib.Path(__file__).resolve().parents[1] / "templates" / "COMPARISON_BASELINE.md"
output_path = REPORTS / "COMPARISON.md"

def find_latest_diag():
    if not REPORTS.exists(): return None
    candidates = [p for p in REPORTS.glob("diagnostic_*") if p.is_dir()]
    if not candidates: return None
    return sorted(candidates)[-1]

def load_json(p):
    try:
        return json.loads(p.read_text())
    except Exception:
        return {}

def table_endpoints(routes_static, routes_runtime):
    rows = []
    # Use runtime if available, else static
    rt = routes_runtime.get("routes") if isinstance(routes_runtime, dict) else None
    if routes_runtime.get("ok") and rt:
        for r in rt:
            methods = ",".join(r.get("methods") or [])
            rows.append([r.get("path",""), methods, r.get("handler",""), "runtime"])
    else:
        for r in routes_static.get("routes", []):
            rows.append([r.get("path",""), r.get("method",""), r.get("function",""), r.get("file","")])
    if not rows:
        return "\n_No endpoints detected._\n"
    header = "| Path | Methods | Handler | Source |\n|---|---|---|---|"
    body = "\n".join(f"| {a} | {b} | {c} | {d} |" for a,b,c,d in rows)
    return header + "\n" + body + "\n"

def list_jobs(jobs):
    files = jobs.get("job_files", [])
    if not files: return "_No job indicators found._\n"
    return "\n".join(f"- {f}" for f in files) + "\n"

def summarize_db(dbj):
    parts = []
    models = dbj.get("db",{}).get("models",[])
    if models:
        parts.append("**Models:** " + ", ".join(sorted(set(m['model'] for m in models))))
    db_files = dbj.get("db",{}).get("db_files",[])
    if db_files:
        parts.append("**SQLite files:** " + ", ".join(db_files))
    fa = ""
    return "- " + "\n- ".join(parts) + ("\n" if parts else "_No DB indicators found._\n")

def summarize_faiss(fj):
    f = fj.get("faiss", {})
    files = f.get("files", []); idx = f.get("index_files", [])
    if not files and not idx: return "_No FAISS usage detected._\n"
    lines = []
    if files: lines.append("**FAISS imports in:** " + ", ".join(files))
    if idx: lines.append("**Index files:** " + ", ".join(idx))
    return "- " + "\n- ".join(lines) + "\n"

def summarize_addon(aj):
    matches = aj.get("matches", [])
    if not matches: return "_No obvious no-code coder files detected._\n"
    return f"_Found {len(matches)} suspected addon-related paths._\n\n" + "\n".join(f"- {m}" for m in matches[:200]) + ("\n" if len(matches)>0 else "")

def infer_actual_status(routes, jobs, dbj):
    # Lightweight heuristics
    has_health = any((r.get("path")=="/api/health") for r in routes.get("routes",[])) if "routes" in routes else False
    ep = {r.get("path",""): r for r in routes.get("routes",[])}
    def _yn(flag): return "Working (detected)" if flag else "Missing/unclear"
    research = any("/api/research" in k for k in ep)
    drafting = any("/api/draft" in k for k in ep)
    repurpose = any("/api/repurpose" in k for k in ep)
    publish = any("/api/publish" in k for k in ep)
    orches = bool(jobs.get("job_files"))
    return {
        "mission": "Observable API with health." if has_health else "Unclear; no health route detected.",
        "research": _yn(research),
        "drafting": _yn(drafting),
        "repurposing": _yn(repurpose),
        "publishing": _yn(publish),
        "orchestration": _yn(orches)
    }

def main():
    latest = find_latest_diag()
    if not latest:
        content = pathlib.Path(baseline_path).read_text()
        content = content.replace("<!-- filled by builder -->", "_No diagnostic folder found. Run scripts/diagnose_all.zsh first._")
        pathlib.Path(output_path).write_text(content)
        print(f"Wrote skeleton comparison to {output_path}")
        return

    rs = load_json(latest / "routes_static.json")
    rr = load_json(latest / "routes_runtime.json")
    jb = load_json(latest / "jobs.json")
    dbj = load_json(latest / "db.json")
    fj = load_json(latest / "faiss.json")
    cfg = load_json(latest / "config.json")
    aj = load_json(latest / "addon_matches.json")

    actual = infer_actual_status(rs if rs.get("routes") else rr, jb, dbj)
    doc = pathlib.Path(baseline_path).read_text()
    doc = doc.replace("<!-- filled by builder -->", actual["mission"])
    doc = doc.replace("<!-- actual.research -->", actual["research"])
    doc = doc.replace("<!-- actual.drafting -->", actual["drafting"])
    doc = doc.replace("<!-- actual.repurposing -->", actual["repurposing"])
    doc = doc.replace("<!-- actual.publishing -->", actual["publishing"])
    doc = doc.replace("<!-- actual.orchestration -->", actual["orchestration"])

    # Endpoints
    doc = doc.replace("<!-- builder will insert a table -->", table_endpoints(rs, rr))

    # Jobs
    doc = doc.replace("<!-- builder will insert a table/list -->", list_jobs(jb))

    # Data stores (SQLite + FAISS)
    ds = summarize_db(dbj) + "\n" + summarize_faiss(fj)
    doc = doc.replace("<!-- builder will summarize SQLite tables, .db files, FAISS indexes -->", ds)

    # Addon
    doc = doc.replace("<!-- builder will summarize pattern matches -->", summarize_addon(aj))

    # Observations
    observations = []
    if aj.get("matches"): observations.append("No-code coder files detected inside repo; consider separation.")
    if not jb.get("job_files"): observations.append("No scheduler/job hints found; orchestration may be inactive.")
    if not rr.get("ok"): observations.append("Runtime route import failed; app may not start or MP_APP_SPEC may differ.")
    if not rs.get("routes"): observations.append("No static routes were detected; API surface unclear.")
    if not observations: observations.append("No major drift indicators from automated signals; review details above.")
    doc = doc.replace("<!-- builder adds observations -->", "\n".join(f"- {x}" for x in observations))

    pathlib.Path(output_path).write_text(doc)
    print(f"Wrote comparison report to {output_path} (from {latest.name})")

if __name__ == "__main__":
    main()
