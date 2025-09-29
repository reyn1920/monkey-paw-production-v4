#!/usr/bin/env python3
# Simple local self-learning logger. Stores prompts/responses/outcomes to SQLite.
import os, sqlite3, time, sys

DB = os.environ.get("RUNTIME_DB", "self_learning/runtime.db")
os.makedirs(os.path.dirname(DB), exist_ok=True)
conn = sqlite3.connect(DB)
conn.execute("""create table if not exists learning(
    id integer primary key,
    ts int,
    context text,
    prompt text,
    response text,
    outcome text
)""")
conn.commit()

def log(context, prompt, response, outcome="unknown"):
    conn.execute("insert into learning(ts,context,prompt,response,outcome) values(?,?,?,?,?)",
                 (int(time.time()), context, prompt, response, outcome))
    conn.commit()

if __name__ == "__main__":
    context = sys.argv[1] if len(sys.argv) > 1 else "general"
    prompt = sys.stdin.read()
    response = "(paste model output here)"
    log(context, prompt, response, "captured")
    print("Logged to", DB)
