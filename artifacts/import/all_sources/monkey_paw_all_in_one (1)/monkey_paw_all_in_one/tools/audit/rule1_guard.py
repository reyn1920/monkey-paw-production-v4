from pathlib import Path
import sys
BANNED = {"production","Production","PRODUCTION","simulation","placeholder","theoretical","demo","mock","fake","sample","test"}
def scan(base: Path) -> int:
    bad = 0
    for p in base.rglob("*"):
        if p.is_file() and p.suffix in {".py",".md",".txt",".json",".sh",".zsh",".html",".css",".js"}:
            try: txt = p.read_text(errors="ignore")
            except Exception: continue
            hits = [w for w in BANNED if w in txt]
            if hits:
                bad += 1
                print(f"[RULE-1] {p} contains: {', '.join(sorted(set(hits)))}")
    return bad
if __name__ == "__main__":
    base = Path(__file__).resolve().parents[2]
    count = scan(base)
    if count:
        print(f"RULE-1 violations: {count}"); sys.exit(1)
    print("RULE-1 clean.")
