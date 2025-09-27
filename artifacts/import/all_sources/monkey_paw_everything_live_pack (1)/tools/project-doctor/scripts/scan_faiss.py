import os, json, sys
root = sys.argv[1] if len(sys.argv)>1 else "."
hits = []
for base, _, files in os.walk(root):
    for f in files:
        if f.endswith(".py"):
            p = os.path.join(base, f)
            try:
                s = open(p, "r", encoding="utf-8", errors="ignore").read()
            except: continue
            if "faiss" in s.lower() or s.find(".index")>=0:
                hits.append(p)
print(json.dumps({"faiss_related": sorted(set(hits))}, indent=2))
