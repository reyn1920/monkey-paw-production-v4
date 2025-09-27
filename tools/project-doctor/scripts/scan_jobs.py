import os, json, sys, re
root = sys.argv[1] if len(sys.argv)>1 else "."
pat = re.compile(r'(APScheduler|BackgroundTasks|add_job|schedule\.)')
hits = []
for base, _, files in os.walk(root):
    for f in files:
        if f.endswith(".py"):
            p = os.path.join(base, f)
            try: s = open(p, "r", encoding="utf-8", errors="ignore").read()
            except: continue
            if pat.search(s):
                hits.append(p)
print(json.dumps({"job_files": sorted(set(hits))}, indent=2))
