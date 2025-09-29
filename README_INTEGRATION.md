# Monkey-Paw Integration Pack v6 — Additive Integration Guide

## Overview
This pack is designed to be merged into your existing app additively (no deletions, no overwrites outside `_mp_integration/`). It provides a FastAPI backend, a single-user dashboard, and copy-based ingestion/merge tools for integrating assets from Google Drive, Downloads, and Desktop.

## Steps

1. **Unzip and Stage**
   - Place the pack anywhere (e.g., Desktop).
   - All content will be copied into `_mp_integration/` at your project root.

2. **Install & Run API**
   - `python3 -m pip install --upgrade pip`
   - `python3 -m pip install -r _mp_integration/backend/requirements.txt`
   - `./_mp_integration/scripts/run_api.sh`
   - Open the dashboard: `open _mp_integration/dashboard/index.html`

3. **Configure Merge**
   - Edit `_mp_integration/merge/merge_config.json`:
     - `current_project_root`: absolute path to your app (e.g., `/Users/thomasbrianreynolds/monkey paw production v4`)
     - `import_paths`: add your Google Drive root, Downloads, Desktop

4. **Ingest & Merge**
   - Ingest: `python3 _mp_integration/merge/ingest_and_stage.py`
   - Merge: `bash _mp_integration/merge/merge_into_current.sh`

5. **Verify**
   - Health: `curl http://127.0.0.1:8000/api/health` → `{"status":"ok"}`
   - Toggle public: POST to `/api/toggle_public`
   - Dashboard: Use ChatGPT↔Gemini convene flow

## Safety & Rollback
- **No-Delete**: No files outside `_mp_integration/` are removed or overwritten.
- **Rollback**: To remove, delete `_mp_integration/` and folders under `imports/`, `integrated_pack/`, `backups/` only.
- **Rule-1**: Vocabulary ban enforced in all added docs/strings.
- **Zero-cost**: No paid/trial services added.
- **Two-pass verification**: Use mutual diagnostics with all AI coders before declaring done.

## VS Code Tasks
- Use the built-in tasks for API, dashboard, ingest, and merge.

---
For any issues, review this README and the pack’s documentation. No deletions or overwrites outside `_mp_integration/` are permitted.
