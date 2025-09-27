import sys, os, re, json, pathlib
words = ["production","simulation","placeholder","theoretical","demo","mock","fake","sample","test"]
pattern = re.compile(r"\b(" + "|".join(map(re.escape, words)) + r")\b", re.IGNORECASE)
root = sys.argv[1] if len(sys.argv)>1 else "."
self_file = str(pathlib.Path(__file__).resolve())
hits = []
for base, _, files in os.walk(root):
    for f in files:
        p = os.path.join(base,f)
        if os.path.samefile(p, self_file):
            continue
        try: s = open(p,"r",encoding="utf-8",errors="ignore").read()
        except: continue
        if pattern.search(s):
            hits.append({"file": p})
print(json.dumps(hits, indent=2))
if hits: sys.exit(2)
