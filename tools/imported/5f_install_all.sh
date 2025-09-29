
#!/usr/bin/env bash
set -euo pipefail
ROOT="${1:-.}"
echo "Installing into: $ROOT"
rsync -a --ignore-existing backend/ "$ROOT/backend/" || true
rsync -a --ignore-existing dashboard/ "$ROOT/dashboard/" || true
rsync -a --ignore-existing tools/ "$ROOT/tools/" || true
rsync -a --ignore-existing assets/ "$ROOT/assets/" || true
rsync -a --ignore-existing scripts/ "$ROOT/scripts/" || true
rsync -a --ignore-existing config/ "$ROOT/config/" || true
rsync -a --ignore-existing docs/ "$ROOT/docs/" || true
rsync -a --ignore-existing qa/ "$ROOT/qa/" || true
rsync -a --ignore-existing docker/ "$ROOT/docker/" || true
rsync -a --ignore-existing http/ "$ROOT/http/" || true
APP="$ROOT/backend/app.py"; mkdir -p "$ROOT/backend"
if [ ! -f "$APP" ]; then echo "from fastapi import FastAPI\napp=FastAPI()" > "$APP"; fi
add() { grep -qF "$1" "$APP" || sed -i.bak "1s|^|$1\n|" "$APP"; }
inc() { grep -qF "$1" "$APP" || printf "\n%s\n" "$1" >> "$APP"; }
add "from channel_presets_router import router as channel_presets_router"
add "from scheduler_router import router as scheduler_router"
add "from compliance_router import router as compliance_router"
add "from manifest_ingest_router import router as manifest_ingest_router"
add "from outro_router import router as outro_router"
add "from status_router import router as status_router"
add "from failsafes_router import router as failsafes_router"
add "from abtest_router import router as abtest_router"
add "from link_rotator_router import router as link_rotator_router"
add "from seo_router import router as seo_router"
add "from health import router as health_router"
add "from integrations_router import router as integrations_router"
add "from dupe_router import router as dupe_router"
add "from captions_router import router as captions_router"
grep -q "FastAPI(" "$APP" || echo "app=FastAPI()" >> "$APP"
inc "app.include_router(channel_presets_router, prefix='/api')"
inc "app.include_router(scheduler_router, prefix='/api')"
inc "app.include_router(compliance_router, prefix='/api')"
inc "app.include_router(manifest_ingest_router, prefix='/api')"
inc "app.include_router(outro_router, prefix='/api')"
inc "app.include_router(status_router, prefix='/api')"
inc "app.include_router(failsafes_router, prefix='/api')"
inc "app.include_router(abtest_router, prefix='/api')"
inc "app.include_router(link_rotator_router, prefix='/api')"
inc "app.include_router(seo_router, prefix='/api')"
inc "app.include_router(health_router, prefix='/api')"
inc "app.include_router(integrations_router, prefix='/api')"
inc "app.include_router(dupe_router, prefix='/api')"
inc "app.include_router(captions_router, prefix='/api')"
python3 -m pip install --upgrade pip >/dev/null
python3 -m pip install fastapi uvicorn pillow >/dev/null
echo "Done. Start with: uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload"
