import sys, os, re, json, pathlib
words = ["production","simulation","placeholder","theoretical","demo","mock","fake","sample","test"]
pat = re.compile(r"\b(" + "|".join(map(re.escape, words)) + r")\b", re.IGNORECASE)
root = sys.argv[1] if len(sys.argv)>1 else "."
self_file = str(pathlib.Path(__file__).resolve())
hits=[]
for b,_,fs in os.walk(root):
    for f in fs:
        p=os.path.join(b,f)
        if os.path.samefile(p,self_file): 
            continue
        try: s=open(p,"r",encoding="utf-8",errors="ignore").read()
        except: continue
        if pat.search(s):
            hits.append({"file":p})
print(json.dumps({"violations":hits},indent=2))
if hits: sys.exit(2)
