#!/usr/bin/env python3
import os
import sys
import json
import sqlite3
import argparse
import re
import datetime
from typing import List, Dict, Any

DEFAULT_DB = os.path.expanduser("~/ONLINE_PRODUCTION/var/research/sources.db")

COLUMNS = [
    "title",
    "domain",
    "url",
    "publisher",
    "content_type",
    "first_seen_utc",
    "last_modified",
    "accessed_utc",
    "why_consulted",
    "relevance",
    "credibility_notes",
    "redirect_of",
    "status",
]

FALLBACK_SCHEMA = """
PRAGMA journal_mode=WAL;
CREATE TABLE IF NOT EXISTS runs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  topic TEXT NOT NULL,
  started_at_utc TEXT NOT NULL,
  ended_at_utc TEXT,
  source_count INTEGER DEFAULT 0,
  notes TEXT
);
CREATE TABLE IF NOT EXISTS sources (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  run_id INTEGER NOT NULL REFERENCES runs(id) ON DELETE CASCADE,
  title TEXT, domain TEXT, url TEXT UNIQUE, publisher TEXT, content_type TEXT,
  first_seen_utc TEXT, last_modified TEXT, accessed_utc TEXT, why_consulted TEXT,
  relevance INTEGER, credibility_notes TEXT, redirect_of TEXT, status TEXT,
  created_at_utc TEXT DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ','now'))
);
CREATE INDEX IF NOT EXISTS idx_sources_run ON sources(run_id);
CREATE INDEX IF NOT EXISTS idx_sources_domain ON sources(domain);
CREATE INDEX IF NOT EXISTS idx_sources_url ON sources(url);
CREATE INDEX IF NOT EXISTS idx_runs_topic ON runs(topic);
"""


def load_markdown_table(path: str) -> List[Dict[str, Any]]:
    text = open(path, "r", encoding="utf-8", errors="ignore").read()
    lines = [l for l in text.splitlines() if l.strip()]
    header_idx = None
    for i, l in enumerate(lines):
        if "|" in l and (
            "Page Title" in l or "Full URL" in l or "Canonical Domain" in l
        ):
            header_idx = i
            break
    if header_idx is None or header_idx + 1 >= len(lines):
        raise RuntimeError("Markdown table not detected")
    header = [h.strip().lower() for h in lines[header_idx].strip("|").split("|")]
    i = header_idx + 1
    if re.search(r"^\s*\|?\s*-{3,}", lines[i]):
        i += 1
    rows = []
    for l in lines[i:]:
        if "|" not in l:
            continue
        cells = [c.strip() for c in l.strip("|").split("|")]
        if len(cells) < len(header):
            cells += [""] * (len(header) - len(cells))
        row = dict(zip(header, cells))
        m = {
            "title": row.get("page title") or row.get("title") or "",
            "domain": row.get("canonical domain") or row.get("domain") or "",
            "url": row.get("full url") or row.get("url") or "",
            "publisher": row.get("publisher/author")
            or row.get("publisher")
            or row.get("author")
            or "",
            "content_type": row.get("content type") or row.get("type") or "",
            "first_seen_utc": row.get("first seen (utc)")
            or row.get("first seen")
            or "",
            "last_modified": row.get("last modified (header/on-page/unknown)")
            or row.get("last modified")
            or "",
            "accessed_utc": row.get("date accessed (utc)")
            or row.get("accessed (utc)")
            or "",
            "why_consulted": row.get("why consulted") or "",
            "relevance": row.get("relevance (0–5)")
            or row.get("relevance (0-5)")
            or row.get("relevance")
            or "",
            "credibility_notes": row.get("credibility notes (≤2 sentences)")
            or row.get("credibility notes")
            or "",
            "redirect_of": row.get("redirect/duplicate of")
            or row.get("duplicate/redirect of")
            or "",
            "status": row.get("status (ok/failed + code)") or row.get("status") or "ok",
        }
        try:
            m["relevance"] = int(str(m["relevance"]).strip() or "0")
        except Exception:
            m["relevance"] = 0
        rows.append(m)
    return rows


def ensure_db(db_path: str):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    with sqlite3.connect(db_path) as con:
        sql_path = os.path.expanduser(
            "~/ONLINE_PRODUCTION/var/research/research_sources_schema.sql"
        )
        if os.path.exists(sql_path):
            con.executescript(open(sql_path, "r", encoding="utf-8").read())
        else:
            con.executescript(FALLBACK_SCHEMA)


def insert_run(con, topic: str, source_count: int, notes: str = "") -> int:
    now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO runs(topic, started_at_utc, ended_at_utc, source_count, notes) VALUES(?,?,?,?,?)",
        (topic, now, now, source_count, notes),
    )
    return cur.lastrowid


def insert_sources(con, run_id: int, sources: List[Dict[str, Any]]):
    cur = con.cursor()
    for s in sources:
        vals = [s.get(k) for k in COLUMNS]
        cur.execute(
            f"""
            INSERT OR IGNORE INTO sources(run_id, {",".join(COLUMNS)})
            VALUES(?, {",".join(["?"]*len(COLUMNS))})
        """,
            [run_id] + vals,
        )


def main():
    ap = argparse.ArgumentParser(
        description="Ingest Gemini Deep Search sources into ONLINE PRODUCTION DB"
    )
    ap.add_argument("--db", default=DEFAULT_DB)
    ap.add_argument("--topic", required=True, help="Research topic label for this run")
    ap.add_argument(
        "--input-json",
        help="Path to JSON array of sources (keys should align with schema)",
    )
    ap.add_argument("--input-md", help="Path to Markdown table of sources to parse")
    args = ap.parse_args()

    if not args.input_json and not args.input_md:
        data = sys.stdin.read()
        try:
            sources = json.loads(data)
        except Exception:
            raise SystemExit("Provide --input-json, --input-md, or JSON on stdin")
    else:
        if args.input_json:
            sources = json.load(open(args.input_json, "r", encoding="utf-8"))
        else:
            sources = load_markdown_table(args.input_md)

    ensure_db(args.db)
    with sqlite3.connect(args.db) as con:
        run_id = insert_run(con, args.topic, len(sources))
        insert_sources(con, run_id, sources)
        con.commit()
        print(
            f"[ingest] run_id={run_id} topic={args.topic!r} sources={len(sources)} db={args.db}"
        )


if __name__ == "__main__":
    main()
