#!/usr/bin/env python3
# Zero-cost scraper with requests + selectolax and SQLite sink.
import os, sqlite3, requests, time
from selectolax.parser import HTMLParser

DB = os.environ.get("RUNTIME_DB", "self_learning/runtime.db")
os.makedirs(os.path.dirname(DB), exist_ok=True)
conn = sqlite3.connect(DB)
conn.execute("create table if not exists pages(url text primary key, title text, fetched_at int, html text)")

def fetch(url):
    headers = {"User-Agent": "Mozilla/5.0 (LocalResearchBot/1.0)"}
    r = requests.get(url, headers=headers, timeout=20)
    r.raise_for_status()
    return r.text

def extract_title(html):
    tree = HTMLParser(html)
    t = tree.css_first("title")
    return t.text().strip() if t else ""

def save(url, html):
    title = extract_title(html)
    conn.execute("insert or replace into pages(url,title,fetched_at,html) values(?,?,?,?)", (url, title, int(time.time()), html))
    conn.commit()

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: scraper.py <url> [<url> ...]")
        raise SystemExit(1)
    for u in sys.argv[1:]:
        try:
            html = fetch(u)
            save(u, html)
            print("OK", u)
        except Exception as e:
            print("ERR", u, e)
