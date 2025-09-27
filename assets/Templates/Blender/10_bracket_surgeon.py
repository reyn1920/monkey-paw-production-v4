#!/usr/bin/env python3
#!/usr/bin/env python3

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP: {".git", ".venv", "venv", "__pycache__", "node_modules", "dist", "build"}


def pyfiles(root: Path):
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in SKIP]
        for f in fn:
            if f.endswith(".py"):
                yield Path(dp) / f


def suspicious(ln: str) -> bool:
    s = ln.strip()
    if not s or s.startswith("#"):
        return False
    # Solo or trailing unmatched closers are common shards
    if s in (")", "]", "}", "),", "],", "},"):
        return True
    # Heuristic: more closers than openers on a line with no obvious opener
    opens = ln.count("(") + ln.count("[") + ln.count("{")
    clos = ln.count(")") + ln.count("]") + ln.count("}")
    return clos > opens and opens == 0


def main():
    for f in pyfiles(ROOT):
        s = f.read_text(encoding="utf-8", errors="replace")
        out = []
        for ln in s.splitlines():
            if suspicious(ln):
                out.append("# BRACKET_SURGEON: disabled\n# " + ln)
            else:
                out.append(ln)
        new = "\n".join(out)
        if new != s:
            f.write_text(new, encoding="utf-8")


# DEBUG_REMOVED: print("[bracket_surgeon] pass complete")

if __name__ == "__main__":
    os.chdir(ROOT)
    main()
