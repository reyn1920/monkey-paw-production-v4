#!/usr/bin/env python3
import os, shutil, socket, sqlite3, datetime, json, sys

LOG = os.path.join(os.path.dirname(__file__), "watchdog.log")
DB_PATH = os.environ.get("WATCHDOG_DB", "self_learning/runtime.db")

def log(entry):
    with open(LOG, "a") as f:
        f.write(f"{datetime.datetime.now().isoformat()} {entry}\n")

def check_port(host, port, timeout=1.0):
    s = socket.socket()
    s.settimeout(timeout)
    try:
        s.connect((host, port))
        s.close()
        return True
    except Exception:
        return False

def disk_ok(path="/"):
    usage = shutil.disk_usage(path)
    pct = usage.free / usage.total
    return pct > 0.1, pct

def sqlite_ok(db_path):
    try:
        conn = sqlite3.connect(db_path)
        conn.execute("pragma integrity_check;")
        conn.close()
        return True
    except Exception as e:
        log(f"[SQLITE]{e}")
        return False

def main():
    checks = {
        "api_8000": check_port("127.0.0.1", 8000),
        "ollama_11434": check_port("127.0.0.1", 11434),
    }
    ok_disk, pct = disk_ok("/")
    checks["disk_ok"] = ok_disk
    checks["disk_free_ratio"] = round(pct, 3)
    checks["sqlite_ok"] = sqlite_ok(DB_PATH)

    log(json.dumps(checks))
    bad = [k for k, v in checks.items() if v in (False, 0)]
    print("OK" if not bad else f"ALERT {bad}")
    sys.exit(0 if not bad else 1)

if __name__ == "__main__":
    main()
