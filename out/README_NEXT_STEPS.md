# Monkey Paw V4 — Download Pack (All You Need)

This folder contains everything to wire true live data, run the app publicly with free tools, and operate the dashboard.

## Public URL & Health
- Public (Cloudflare Quick Tunnel): run `zsh scripts/run_public.zsh` and copy the printed URL.
- Local: http://127.0.0.1:8000/
- Health: GET `/api/health`

## Live Data for Dashboard (Revenue + KPIs)
- Edit `config/sheets.yaml` or use the UI button "Set Sheets URLs" at `/`.
- Requires TWO CSV tabs (public, no auth):
  - `revenue_daily`: columns `day, goal, actual`
  - `content_kpis`: columns `metric, value`
- CSV URL format:
  `https://docs.google.com/spreadsheets/d/SHEET_ID/gviz/tq?tqx=out:csv&sheet=TAB_NAME`
- Quick set via API:
```bash
curl -sS -X POST "http://127.0.0.1:8000/api/admin/update_sheets" \
  -H 'Content-Type: application/json' \
  -d '{
    "revenue_csv_url": "https://docs.google.com/spreadsheets/d/<ID>/gviz/tq?tqx=out:csv&sheet=revenue_daily",
    "content_kpis_csv_url": "https://docs.google.com/spreadsheets/d/<ID>/gviz/tq?tqx=out:csv&sheet=content_kpis",
    "poll_seconds": 60
  }'

curl -sS -X POST "http://127.0.0.1:8000/api/admin/refresh_data"
```
- Timeframe selector (uses your computer date): `GET /api/metrics/revenue?days=7|30|60`.

## Multi-Source Sheets (Voices + Right Perspective)
- Edit `config/sheets_multi.json` with real Sheet URLs and tab names (see `sheets_multi_example.json`).
- Endpoints:
  - List: `GET /api/sheets/config`
  - Fetch: `GET /api/sheets/{source}/{key}`
  - Legacy default: `GET /api/sheets/{key}`
- Verify samples are in `curl_samples.sh`.

## Database (SQLite)
- File: `db/monkey_paw.db`
- Tables:
  - `revenue_daily(day TEXT PRIMARY KEY, goal REAL, actual REAL)`
  - `content_kpis(metric TEXT PRIMARY KEY, value INTEGER)`
- Schema is auto-ensured at app startup.
- Health queries:
```bash
sqlite3 db/monkey_paw.db "SELECT COUNT(*), MIN(day), MAX(day) FROM revenue_daily;"
sqlite3 db/monkey_paw.db "SELECT metric, value FROM content_kpis;"
```

## Run Commands
- Public dev tunnel:
```bash
zsh scripts/run_public.zsh
# Logs: /tmp/monkey_paw_v4_uvicorn.log, /tmp/cloudflared_monkeypaw.log
```
- Watchdog (keeps both up):
```bash
zsh scripts/watchdog.zsh
# Log: /tmp/monkeypaw_watchdog.log
```

## Security & Free-Only Notes
- Use public Sheets with no secrets (mirror if needed).
- Cloudflare Quick Tunnel is free for dev; rotate URL if sharing widely.
- No API keys required for Sheets CSV export.

## Troubleshooting
- 403 Upstream fetch error → Publish Sheet/tab to web or set to "Anyone with link can view".
- 404 Unknown source/tab → Fix names in `config/sheets_multi.json`.
- Empty chart → Ensure required headers and at least one data row.
- Slow Sheets → Raise `ttl_seconds` in `config/sheets_multi.json`.

## What to send me to finalize
- Dashboard: two CSV URLs (revenue_daily, content_kpis).
- Multi-source: Voices & Right Perspective Sheet URLs + exact tab names.
