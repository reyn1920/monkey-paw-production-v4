# Monkey Paw — Core

Goal: focus on automated research → drafting → repurposing → publishing.

This folder includes:
- `app/` — minimal API scaffold and health endpoint.
- `config/features.yaml` — toggles including `nocode_stack_enabled` (default: false).

Run locally (example):
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
# then check http://127.0.0.1:8000/api/health
```
