#!/usr/bin/env python3
import os, re, sys, json, pathlib
ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
jobs = []
pat = re.compile(r'(APScheduler|BackgroundTasks|add_job|scheduler\.add_job|@repeat|schedule\.every\(|celery|rq\.Queue)', re.I)
for py in ROOT.rglob("*.py"):
    try: t = py.read_text(errors="ignore")
    except Exception: continue
    if pat.search(t): jobs.append(str(py.relative_to(ROOT)))
print(json.dumps({"root": str(ROOT), "job_files": jobs}, indent=2))
