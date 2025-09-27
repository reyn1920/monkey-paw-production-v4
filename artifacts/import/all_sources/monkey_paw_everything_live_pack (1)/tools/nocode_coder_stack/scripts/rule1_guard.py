import sys, os, json, re, pathlib
words = ["production","simulation","placeholder","theoretical","demo","mock","fake","sample","test"]
pattern = re.compile(r"\b(" + "|".join(map(re.escape, words)) + r")\b", re.IGNORECASE)
root = sys.argv[1] if len(sys.argv)>1 else "."
self_file = str(pathlib.Path(__file__).resolve())

hits = []
for base, _, files in os.walk(root):
    for f in files:
        if any(f.endswith(ext) for ext in [".py",".js",".ts",".json",".md",".txt",".yaml",".yml",".toml",".ini",".cfg",".html",".css"]):
            p = os.path.join(base,f)
            # ignore this guard file itself
            if os.path.samefile(p, self_file):
                continue
            try: s = open(p,"r",encoding="utf-8",errors="ignore").read()
            except: continue
            for m in pattern.finditer(s):
                hits.append({"file": p, "word": m.group(1)})
                break
print(json.dumps({"violations": hits}, indent=2))
if hits:
    sys.exit(2)
