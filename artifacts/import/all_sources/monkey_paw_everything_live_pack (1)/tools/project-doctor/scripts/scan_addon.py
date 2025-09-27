import os, json, sys, re
root = sys.argv[1] if len(sys.argv)>1 else "."
patterns = [r"nocode", r"lowcode", r"agent[-_/]?builder", r"prompt[-_]?builder", r"autocoder"]
hits = []
for base, _, files in os.walk(root):
    for f in files:
        p = os.path.join(base, f)
        try:
            s = open(p, "r", encoding="utf-8", errors="ignore").read()
        except:
            s = ""
        name = f.lower()
        hay = name + " " + s.lower()
        for pat in patterns:
            if re.search(pat, hay):
                hits.append(p)
                break
print(json.dumps({"addon_like_files": sorted(set(hits))}, indent=2))
