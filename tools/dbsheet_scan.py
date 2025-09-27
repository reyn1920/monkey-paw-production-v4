from __future__ import annotations
import os, re, json, csv
from pathlib import Path
from typing import Dict, List, Any

ROOT = Path(os.environ.get("SCAN_ROOT", ".")).resolve()

# Patterns for DB URIs
PATTERNS = {
    "sqlite": re.compile(r"sqlite(?:\+pysqlite)?:///(.+?\.db)\b"),
    "postgres": re.compile(r"postgres(?:ql)?://[^\s\"']+"),
    "mysql": re.compile(r"mysql(?:\+pymysql)?://[^\s\"']+"),
    "mongo": re.compile(r"mongodb(?:\+srv)?://[^\s\"']+"),
    "bigquery": re.compile(r"bigquery://[^\s\"']+"),
    "firestore": re.compile(r"(?:FIREBASE_|GOOGLE_APPLICATION_CREDENTIALS|FIRESTORE_)[A-Z0-9_]*"),
}

# Common file names for env/config
ENV_HINTS = [
    ".env", ".env.local", ".envrc", "dotenv", "config.env",
    "settings.json", "settings.yaml", "settings.yml",
    "config.json", "config.yaml", "config.yml",
    "database.json", "database.yaml", "database.yml",
]

# Google Sheets: match either /spreadsheets/d/<ID> or direct gviz export
SHEET_RE = re.compile(r"https://docs\\.google\\.com/spreadsheets/d/([a-zA-Z0-9-_]+)[^\s\"'>]*")
GVIZ_SHEET_RE = re.compile(r"[?&]sheet=([^&\s\"'>]+)")
GID_RE = re.compile(r"[?&#]gid=(\d+)")

# Quick file filters
TEXT_EXT = {".py",".ts",".tsx",".js",".jsx",".md",".json",".yaml",".yml",".toml",".ini",".txt",".env",".sh",".zsh",".cfg",".conf",".html",".css"}
BIN_SKIP_EXT = {".png",".jpg",".jpeg",".gif",".webp",".mp4",".mov",".pdf",".zip",".gz",".bz2",".xz",".7z",".dylib",".so",".a",".o",".ttf",".woff",".woff2"}

def is_textlike(p: Path) -> bool:
    ext = p.suffix.lower()
    if ext in BIN_SKIP_EXT: return False
    if ext in TEXT_EXT: return True
    try:
        if p.stat().st_size < 2_000_000:
            with p.open("rb") as f:
                chunk = f.read(1024)
            return b"\0" not in chunk
    except Exception:
        return False
    return False

def find_sqlite_files() -> List[str]:
    out = []
    for p in ROOT.rglob("*.db"):
        try:
            out.append(str(p.relative_to(ROOT)))
        except Exception:
            out.append(str(p))
    return out

def scan_text() -> Dict[str, Any]:
    db_hits: List[Dict[str, Any]] = []
    sheet_hits: Dict[str, Dict[str, Any]] = {}

    for p in ROOT.rglob("*"):
        if not p.is_file(): continue
        if not is_textlike(p): continue
        try:
            text = p.read_text("utf-8", errors="replace")
        except Exception:
            continue

        # DB URIs
        for name, rx in PATTERNS.items():
            for m in rx.finditer(text):
                val = m.group(0)
                db_hits.append({
                    "engine": name,
                    "value": val,
                    "file": str(p.relative_to(ROOT)),
                })

        # SQLite paths in code like 'sqlite:///path/to.db'
        for m in re.finditer(r"sqlite:///([^\s\"']+\.db)", text):
            db_hits.append({
                "engine": "sqlite",
                "value": "sqlite:///" + m.group(1),
                "file": str(p.relative_to(ROOT)),
            })

        # Google Sheets
        for m in SHEET_RE.finditer(text):
            sheet_url = m.group(0)
            sid = m.group(1)
            entry = sheet_hits.setdefault(sid, {"sheet_url": sheet_url, "files": set(), "tabs": set(), "gids": set()})
            entry["files"].add(str(p.relative_to(ROOT)))
            # Infer tabs
            for sm in GVIZ_SHEET_RE.finditer(text):
                entry["tabs"].add(sm.group(1))
            for gm in GID_RE.finditer(text):
                entry["gids"].add(gm.group(1))

    # attach discovered .db files even if no URI string was found
    for db in find_sqlite_files():
        db_hits.append({"engine": "sqlite", "value": f"sqlite:///{db}", "file": db})

    # finalize sets
    for sid, d in sheet_hits.items():
        d["files"] = sorted(d["files"])
        d["tabs"] = sorted(d["tabs"])
        d["gids"] = sorted(d["gids"])

    return {"db_hits": db_hits, "sheet_hits": sheet_hits}

def write_outputs(results: Dict[str, Any]) -> None:
    os.makedirs("out", exist_ok=True)

    # JSON DB inventory
    dbs = results["db_hits"]
    with open("out/db_inventory.json", "w", encoding="utf-8") as f:
        json.dump(dbs, f, indent=2, ensure_ascii=False)

    # JSON Sheets inventory
    sheets = []
    for sid, d in results["sheet_hits"].items():
        sheets.append({
            "sheet_id": sid,
            "sheet_url": d["sheet_url"],
            "inferred_tabs": d["tabs"],
            "gids": d["gids"],
            "found_in_files": d["files"],
        })
    with open("out/sheets_inventory.json", "w", encoding="utf-8") as f:
        json.dump(sheets, f, indent=2, ensure_ascii=False)

    # Flat CSV
    with open("out/dbsheet_inventory.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["type","engine_or_id","value_or_url","file_or_tabs"])
        for d in dbs:
            w.writerow(["db", d["engine"], d["value"], d["file"]])
        for s in sheets:
            w.writerow(["sheet", s["sheet_id"], s["sheet_url"], "|".join(s["inferred_tabs"]) or "|".join(s["gids"])])

    # Autogenerate multi-source snippet if sheets were found
    if sheets:
        sources = {}
        for s in sheets:
            name = "source_" + s["sheet_id"][:6].lower()
            tabs = {}
            for t in s["inferred_tabs"]:
                tabs[t.lower()] = {"tab_name": t, "ttl_seconds": 300}
            sources[name] = {"sheet_url": s["sheet_url"], "tabs": tabs}
        with open("out/next_steps.txt", "w", encoding="utf-8") as f:
            f.write("Suggested config/sheets_multi.json sources snippet:\n\n")
            f.write(json.dumps({"sources": sources}, indent=2))
            f.write("\n\nVerify with curl (examples):\n")
            for src in sources.keys():
                for key in list(sources[src]["tabs"].keys())[:2]:
                    f.write(f"curl -sS http://127.0.0.1:8000/api/sheets/{src}/{key} | jq\n")
    else:
        with open("out/next_steps.txt", "w", encoding="utf-8") as f:
            f.write("No Google Sheets URLs found in scanned files.\n")
            f.write("Add your Sheet URLs to config, or share them so I can wire them for you.\n")

def main():
    results = scan_text()
    write_outputs(results)
    print("Scan complete. See out/db_inventory.json, out/sheets_inventory.json, out/dbsheet_inventory.csv, out/next_steps.txt")

if __name__ == "__main__":
    main()
