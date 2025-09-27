# Monkey Paw Productions V3 — Cursor Task Plan

This plan tells Cursor exactly what to do to make the app fully live without user intervention.

## 0) Project Open
- Open the folder in Cursor.
- Ensure integrated terminal is available.

## 1) Install & Launch
- Run: `zsh install_and_launch.zsh`
- Verify the dashboard is reachable at http://127.0.0.1:8000/

## 2) Sanity Checks
- Run task **Audit: Two Pass** (or `zsh tools/audit/run_two_pass_audit.zsh`).
- Run task **Missing Info Audit (Monkey Paw)** (or `zsh scripts/first_run/fill_missing_info.zsh`).
- Confirm `reports/` generated without blocking errors.

## 3) Import Assets (Optional, if provided)
- For writing: `zsh tools/importers/import_writing.zsh ~/Documents/Writing`
- For thumbnails: `zsh tools/importers/import_thumbnails.zsh ~/Pictures`
- For marketing docs: `zsh tools/importers/import_marketing.zsh ~/Documents`
- For analytics CSVs: `python3 tools/importers/import_analytics.py ~/Downloads`

## 4) YouTube + Book + Digital Kit
- Create a first draft: `echo "My V3 draft" > artifacts/staging/draft_youtube.txt`
- Run task **YouTube Prep+Upload**
- Run task **Build EPUB**
- Run task **Build Digital Kit**
- Confirm outputs in `artifacts/published/`

## 5) Approval & Publishing (Guarded)
- Ensure panic is OFF: `zsh scripts/panic_off.zsh`
- Approve: `curl -s http://127.0.0.1:8000/api/admin/approve_publish/true | python3 -m json.tool`
- Publish: `curl -s -X POST http://127.0.0.1:8000/api/publish | python3 -m json.tool`

## 6) Backup & Watchdog
- Backup snapshot: `zsh tools/snapshots/backup_now.zsh`
- Launch watchdog in background: `zsh tools/watchdog/health_loop.zsh &`

## 7) Done
- Confirm dashboard charts (Revenue vs Goal), KPIs, and Plan viewer.
- Provide logs: `/tmp/monkey_paw_v3_uvicorn.log`
