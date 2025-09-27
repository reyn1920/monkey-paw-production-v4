#!/usr/bin/env python3
import os
import sqlite3
import argparse
import json

DEFAULT_DB = os.path.expanduser("~/ONLINE_PRODUCTION/var/research/sources.db")


def main():
    ap = argparse.ArgumentParser(description="Query ONLINE PRODUCTION research DB")
    ap.add_argument("--db", default=DEFAULT_DB)
    ap.add_argument("--topic", help="Filter by topic (LIKE)")
    ap.add_argument("--domain", help="Filter by domain (LIKE)")
    ap.add_argument("--last-runs", type=int, help="Show last N runs")
    ap.add_argument("--top-domains", type=int, help="Show top N domains overall")
    ap.add_argument("--export-json", help="Export query result to JSON file")
    args = ap.parse_args()

    con = sqlite3.connect(args.db)
    cur = con.cursor()

    result = {}
    if args.last_runs:
        cur.execute(
            "SELECT id, topic, started_at_utc, ended_at_utc, source_count FROM runs ORDER BY id DESC LIMIT ?",
            (args.last_runs,),
        )
        result["runs"] = [
            {
                "id": r[0],
                "topic": r[1],
                "started_at": r[2],
                "ended_at": r[3],
                "sources": r[4],
            }
            for r in cur.fetchall()
        ]

    where = []
    params = []
    if args.topic:
        where.append("topic LIKE ?")
        params.append(f"%{args.topic}%")
    if args.domain:
        where.append("domain LIKE ?")
        params.append(f"%{args.domain}%")
    q = "SELECT title,domain,url,publisher,content_type,accessed_utc,relevance FROM sources"
    if where:
        q += " WHERE " + " AND ".join(where)
    q += " ORDER BY id DESC LIMIT 200"
    cur.execute(q, params)
    result["sources"] = [
        {
            "title": r[0],
            "domain": r[1],
            "url": r[2],
            "publisher": r[3],
            "type": r[4],
            "accessed_utc": r[5],
            "relevance": r[6],
        }
        for r in cur.fetchall()
    ]

    if args.top_domains:
        cur.execute(
            "SELECT domain, COUNT(1) c FROM sources GROUP BY domain ORDER BY c DESC LIMIT ?",
            (args.top_domains,),
        )
        result["top_domains"] = [
            {"domain": r[0], "count": r[1]} for r in cur.fetchall()
        ]

    out = json.dumps(result, indent=2)
    if args.export_json:
        open(args.export_json, "w", encoding="utf-8").write(out)
        print(f"[export] {args.export_json}")
    else:
        print(out)


if __name__ == "__main__":
    main()
