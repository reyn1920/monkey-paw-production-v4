#!/usr/bin/env python3
import os
import sqlite3
import glob

DB_PATH = os.environ.get(
    "TRAE_DB_PATH", os.path.join(os.getcwd(), "data", "trae_ai.db")
)
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS schema_migrations (name TEXT PRIMARY KEY, applied_at DATETIME DEFAULT CURRENT_TIMESTAMP)"
    )
    for f in sorted(glob.glob(os.path.join("migrations", "*.sql"))):
        name = os.path.basename(f)
        if conn.execute(
            "SELECT 1 FROM schema_migrations WHERE name=?", (name,)
        ).fetchone():
            continue
        with open(f, encoding="utf-8") as fh:
            sql = fh.read()
        conn.executescript(sql)
        conn.execute("INSERT OR IGNORE INTO schema_migrations(name) VALUES(?)", (name,))
        conn.commit()
        print("applied", name)
    conn.close()


if __name__ == "__main__":
    main()
