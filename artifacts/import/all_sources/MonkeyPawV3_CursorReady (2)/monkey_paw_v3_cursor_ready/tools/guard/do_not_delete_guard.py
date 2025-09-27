from pathlib import Path
import sys, yaml
BASE = Path(__file__).resolve().parents[2]
CFG = BASE / "config" / "do_not_delete.yaml"
LOG = BASE / "reports" / "DO_NOT_DELETE_REPORT.txt"
def main():
    if not CFG.exists(): return 0
    data = yaml.safe_load(CFG.read_text()) or {}
    kws = set((data.get("keywords") or []))
    hits = []
    for p in BASE.rglob("*"):
        s = str(p)
        for k in kws:
            if k and k.lower() in s.lower():
                hits.append(s); break
    LOG.parent.mkdir(parents=True, exist_ok=True)
    LOG.write_text("\n".join(sorted(set(hits))) + "\n")
    print(f"Guard scan complete. {len(set(hits))} protected references tracked."); return 0
if __name__ == "__main__": sys.exit(main())
