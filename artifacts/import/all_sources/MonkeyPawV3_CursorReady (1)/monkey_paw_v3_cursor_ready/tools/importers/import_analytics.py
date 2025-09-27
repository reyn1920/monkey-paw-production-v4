from pathlib import Path
import csv, sys, sqlite3
BASE = Path(__file__).resolve().parents[2]
DB = BASE / "db" / "monkey_paw_guard.db"
SCHEMA = {
    "yt_metrics": "create table if not exists yt_metrics (id integer primary key, date text, views int, watch_hours real, subs int, revenue_cents int)",
    "newsletter": "create table if not exists newsletter (id integer primary key, date text, subs int, opens int, clicks int)",
}
def ensure_schema(con):
    cur = con.cursor()
    for sql in SCHEMA.values(): cur.execute(sql)
    con.commit()
def import_csv(con, path: Path):
    name = path.stem.lower(); cur = con.cursor()
    if "youtube" in name or "yt" in name:
        for row in csv.DictReader(path.open()):
            cur.execute("insert into yt_metrics(date,views,watch_hours,subs,revenue_cents) values(?,?,?,?,?)",
                        (row.get("date"), int(row.get("views",0)), float(row.get("watch_hours",0)), int(row.get("subs",0)), int(row.get("revenue_cents",0))))
    elif "beehiiv" in name or "newsletter" in name:
        for row in csv.DictReader(path.open()):
            cur.execute("insert into newsletter(date,subs,opens,clicks) values(?,?,?,?)",
                        (row.get("date"), int(row.get("subs",0)), int(row.get("opens",0)), int(row.get("clicks",0))))
    con.commit()
def main(folder: str):
    con = sqlite3.connect(DB); ensure_schema(con)
    p = Path(folder); 
    for f in p.glob("*.csv"): import_csv(con, f)
    con.close(); print(f"Imported CSVs from {folder} into {DB}")
if __name__ == "__main__": main(sys.argv[1] if len(sys.argv)>1 else str(BASE/"reports"))
