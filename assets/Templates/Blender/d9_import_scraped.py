#!/usr/bin/env python3
import sys
import json
import sqlite3
import os

DB = os.getenv("DB_PATH", "data/base44.sqlite")


def ensure(con):
    con.executescript(
        "CREATE TABLE IF NOT EXISTS voices(id INTEGER PRIMARY KEY AUTOINCREMENT,source TEXT,voice_id TEXT,name TEXT,gender TEXT,lang TEXT,meta TEXT);CREATE TABLE IF NOT EXISTS items(id INTEGER PRIMARY KEY AUTOINCREMENT,category TEXT,title TEXT,content TEXT,path TEXT,meta TEXT);"
    )
    con.commit()


def main(p):
    data = json.load(open(p, encoding="utf-8"))
    con = sqlite3.connect(DB)
    ensure(con)
    for v in data.get("voices", []):
        con.execute(
            "INSERT INTO voices(source,voice_id,name,gender,lang,meta) VALUES(?,?,?,?,?,?)",
            (
                v.get("source", "other"),
                v.get("voice_id"),
                v.get("name"),
                v.get("gender"),
                v.get("lang"),
                json.dumps(v.get("meta", {})),
            ),
        )
    for i in data.get("items", []):
        con.execute(
            "INSERT INTO items(category,title,content,path,meta) VALUES(?,?,?,?,?)",
            (
                i.get("category", "misc"),
                i["title"],
                i.get("content", ""),
                i.get("path", ""),
                json.dumps(i.get("meta", {})),
            ),
        )
    con.commit()
    print(
        "imported voices",
        len(data.get("voices", [])),
        "items",
        len(data.get("items", [])),
    )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python utils/import_scraped.py scraped.json")
        sys.exit(2)
    main(sys.argv[1])
