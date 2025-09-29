#!/usr/bin/env python3
#!/usr/bin/env python3

import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP: {".git", ".venv", "venv", "__pycache__", "node_modules", "dist", "build"}

BLOCK = re.compile(
    r"^\s*(def|class|if|elif|else|for|while|try|except|finally|with)\b.*:\s*(#.*)?$"
)


def pyfiles(root: Path):
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in SKIP]
        for f in fn:
            if f.endswith(".py"):
                yield Path(dp) / f


def norm(ws: str) -> str:
    return ws.replace("\t", "    ")


def heal(p: Path):
    s = p.read_text(encoding="utf-8", errors="replace")
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    lines = [norm(ln.rstrip()) for ln in s.split("\n")]

    # Remove leading indentation from file start until a non-empty appears (common paste artifact)
    i = 0
    while i < len(lines) and lines[i].startswith("    ") and lines[i].strip():
        lines[i] = lines[i].lstrip()
        i += 1

    # Insert 'pass' for empty suites (sibling or EOF immediately after a block)
    out = []
    n = len(lines)
    idx = 0
    while idx < n:
        out.append(lines[idx])
        if BLOCK.match(lines[idx]):
            indent = len(lines[idx]) - len(lines[idx].lstrip(" "))
            j = idx + 1
            while j < n and (not lines[j].strip() or lines[j].lstrip().startswith("#")):
                j += 1
            if j >= n or (len(lines[j]) - len(lines[j].lstrip(" ")) <= indent):
                out.append(" " * (indent + 4) + "pass")
        idx += 1

    new = "\n".join(out)
    if new != s:
        p.write_text(new, encoding="utf-8")


def main():
    for f in pyfiles(ROOT):
        heal(f)


# DEBUG_REMOVED: print("[indent_healer] pass complete")

if __name__ == "__main__":
    os.chdir(ROOT)
    main()
