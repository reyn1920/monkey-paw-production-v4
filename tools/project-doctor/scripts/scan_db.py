import os, json, sys, re
root = sys.argv[1] if len(sys.argv)>1 else "."
pat = re.compile(r'(SQLModel|create_engine|sqlite3|\.db\b)')
hits = []
for base, _, files in os.walk(root):
    for f in files:
        if f.endswith(".py") or f.endswith(".db"):
            p = os.path.join(base, f)
            try:
                s = open(p, "r", encoding="utf-8", errors="ignore").read() if f.endswith(".py") else ""
            except: s=""
            if f.endswith(".db") or pat.search(s):
                hits.append(p)
print(json.dumps({"db_related": sorted(set(hits))}, indent=2))
