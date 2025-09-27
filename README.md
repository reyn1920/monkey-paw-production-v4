# Monkey Paw V4 — FastAPI App

This repo contains the Monkey Paw V4 FastAPI backend and a lightweight dashboard.

- App URL (local): http://127.0.0.1:8000/
- Health endpoint: GET /api/health
- Static assets: `app/static/`
- Templates: `app/templates/`
- Database: `db/monkey_paw.db` (SQLite)

## Prerequisites
- Python 3.10+ recommended
- macOS (scripts use zsh). Linux works with minor tweaks.
- Optional: `cloudflared` for a free public dev URL
- Optional: `ffmpeg` for media assembly acceleration (fallbacks exist)

## Quick Start (Local)
```bash
# From repo root
zsh scripts/run_server.zsh
# Then open http://127.0.0.1:8000/
```

## Quick Start (Free Public Dev URL)
```bash
# Requires cloudflared installed: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/get-started/cloudflared-installation/
zsh scripts/run_public.zsh
# Copy the printed https://xxxx.trycloudflare.com URL
```

Logs:
- Uvicorn: /tmp/monkey_paw_v4_uvicorn.log
- Cloudflared: /tmp/cloudflared_monkeypaw.log

Watchdog (optional, keeps both alive):
```bash
zsh scripts/watchdog.zsh
```

## Configure Live Dashboard Data (Google Sheets CSV)
The dashboard reads two CSV tabs from a Google Sheet made public (or “Anyone with link can view”). Expected columns:
- `revenue_daily`: `day, goal, actual`
- `content_kpis`: `metric, value`

Set via API:
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
You can also configure from the dashboard UI at `/`.

## Smoke Tests
```bash
# Health
curl -sS http://127.0.0.1:8000/api/health | jq .

# Revenue metrics (last 7 days)
curl -sS "http://127.0.0.1:8000/api/metrics/revenue?days=7" | jq .

# Enqueue a demo job
curl -sS -X POST "http://127.0.0.1:8000/api/jobs/enqueue" \
  -H 'Content-Type: application/json' \
  -d '{"type":"full_video","channel":"right_perspective","payload_json":{"topic":"demo"}}' | jq .
```

## Notes on Free-Only Stack
- No API keys required (uses public Sheets CSV exports).
- Cloudflare Quick Tunnel provides a free dev URL; rotate when sharing widely.
- ffmpeg optional; the app falls back to tiny stub files if unavailable.

## Project Structure
```
app/
  main.py              # FastAPI app, routes, background workers
  routers/
  static/
  templates/
config/
  sheets.yaml          # Dashboard CSV config (auto-created/edited)
  policy.yaml          # Governance policy (free-only defaults enforced)
  sheets_multi.json    # Multi-source config for Sheets-powered fetcher
scripts/
  run_server.zsh       # Local dev (127.0.0.1:8000)
  run_public.zsh       # Public dev URL with Cloudflare Quick Tunnel
  watchdog.zsh         # Optional supervisor for app + tunnel
out/README_NEXT_STEPS.md  # Additional usage notes
```

## Troubleshooting
- 403 on CSV fetch: publish the Google Sheet or set to "Anyone with link can view".
- Empty charts: ensure headers and at least one data row in each tab.
- No public URL: check `/tmp/cloudflared_monkeypaw.log`.
- App not responding: check `/tmp/monkey_paw_v4_uvicorn.log`.
