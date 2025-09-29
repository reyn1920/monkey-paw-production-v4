#!/usr/bin/env bash
set -euo pipefail

export TRAE_CI=${TRAE_CI:-1}
export FAST_MODE=${FAST_MODE:-1}
export CAP_REEL_MINUTES=${CAP_REEL_MINUTES:-1}

echo "🚀 CI-Fast: Starting deterministic test run..."
echo "🧹 Cleaning previous test artifacts..."
mkdir -p assets/releases assets/temp
find assets/releases -type f -name '*.mp4' -mtime +1 -delete || true
find assets/temp -type f -mtime +1 -delete || true

# Pick a timeout command if available; shim if not
TIMEOUT_CMD=""
if command -v timeout >/dev/null 2>&1; then
  TIMEOUT_CMD="timeout"
elif command -v gtimeout >/dev/null 2>&1; then
  TIMEOUT_CMD="gtimeout"
else
  echo "⚠️  No timeout command available, running without timeout"
fi

# Run migrations if present (non-fatal)
python - <<'PY' || true
try:
    from infra.migrations import run_all
    run_all()
    print("[Migrations] OK")
except Exception as e:
    print("[Migrations] skipped:", e)
PY

echo "⏱️  Running tests..."
if [ -n "$TIMEOUT_CMD" ]; then
  $TIMEOUT_CMD 90 python tests/test_final_verification.py
else
  python tests/test_final_verification.py
fi
echo "✅ CI-Fast tests completed"
