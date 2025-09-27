#!/usr/bin/env python3
import sys, re, pathlib, json
BANNED = [r"\bproduction\b", r"\bProduction\b", r"\bPRODUCTION\b", r"\bsimulation\b", r"\bplaceholder\b", r"\btheoretical\b", r"\bdemo\b", r"\bmock\b", r"\bfake\b", r"\bsample\b"]
ROOT = pathlib.Path(sys.argv[1] if len(sys.argv)>1 else ".").resolve()
hits = []
for p in ROOT.rglob("*"):
    if p.is_dir(): continue
    if p.suffix.lower() in {".py",".md",".txt",".yml",".yaml",".json",".toml",".ini",".sh",".zsh",".js",".ts",".html",".css"}:
        try: t = p.read_text(errors="ignore")
        except Exception: continue
        for pat in BANNED:
            for m in re.finditer(pat, t):
                hits.append({"file": str(p.relative_to(ROOT)), "word": re.compile(pat).pattern, "pos": m.start()})
print(json.dumps({"rule1_hits": hits}, indent=2))
sys.exit(1 if hits else 0)
