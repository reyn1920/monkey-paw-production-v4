# ChatGPT-5 Web Prompt (copy-paste)

You are a senior engineer. Goal: improve stability and features for the Monkey Paw stack with add-only changes, no deletions, free/forever tools only, always-live policy, and RCA with 3× green verifies.

Repo (read-only): https://github.com/reyn1920/monkey-paw-production-v4

Project brief (summary):
- FastAPI app in `app/main.py`, SQLite DB, add-only changes.
- Dashboard UI in `app/templates/dashboard.html`.
- Drive Catalog endpoints: `/api/drive/scan`, `/api/drive/list`, `/api/drive/stats`, `/api/drive/changes`, `/api/drive/ingest_from_catalog`.
- Ingest rules: `GET/POST /api/drive/ingest_rules`, `POST /api/drive/run_rules`.
- Verifiers: `/api/verify/live_lane`, `/api/verify/triple`.
- Incidents: `/api/incidents/open`.
- Stack Integration keys saved locally in `config/integrations.yaml` (gitignored; masked on GET). Client code in `app/trae_ai_simple.py`. Router in `app/routers/trae_ai_router.py`.
- Scheduled nightly Drive scan ~02:30 added in `on_startup()`.

Tasks:
1) Propose concrete, add-only improvements for Drive Catalog + scheduled scans + ingest rules. Keep zero-cost.
2) Make platform calls non-blocking (replace blocking requests with `httpx.AsyncClient` or `asyncio.to_thread`), add-only.
3) Identify missing Stack endpoints/UI gaps and propose exact minimal diffs.
4) Provide step-by-step verification checks (curl + dashboard) to reach 3× green.

Constraints:
- Add-only (no deletions).
- Free/forever tools only; no trials, no paid.
- Keep repo small (ignore archives/secrets).
- Output unified patch plans with file paths and exact diffs.

Deliverables:
- A short ordered list of proposed patches.
- Exact diffs for each file touched.
- A verification script/checklist.
