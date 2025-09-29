#!/usr/bin/env bash
set -euo pipefail

# Canonical dir
: "${APP_DIR:=$HOME/ONLINPRDUCTION}"
REPO_DIR="$APP_DIR/repo"
# NOTE: Repo remote name contains 'online-production' by design. We do not rename it.
CLONE_URL="https://github.com/reyn1920/online-production.git"

echo "[Anti-Loop Installer] Using APP_DIR=$APP_DIR"

mkdir -p "$APP_DIR" "$APP_DIR/var/runtime"
# Clone if missing
if [ ! -d "$REPO_DIR/.git" ]; then
  echo "[Anti-Loop Installer] Cloning repo..."
  git clone "$CLONE_URL" "$REPO_DIR"
else
  echo "[Anti-Loop Installer] Repo already present, pulling latest..."
  (cd "$REPO_DIR" && git pull --ff-only || true)
fi

# Create friendly aliases (add-only)
cd "$HOME"
[ -e "online_production" ] || ln -s "ONLINPRDUCTION/repo" "online_production"
[ -e "online-production" ] || ln -s "ONLINPRDUCTION/repo" "online-production"
[ -e "online production" ] || ln -s "ONLINPRDUCTION/repo" "online production"

# Copy anti-loop files into repo
cd "$REPO_DIR"
mkdir -p backend/utils backend/agents/middleware config scripts var/runtime
cp -f "../bundle/backend/utils/loop_guard.py" backend/utils/loop_guard.py
cp -f "../bundle/backend/agents/middleware/guarded_runner.py" backend/agents/middleware/guarded_runner.py
cp -f "../bundle/sitecustomize.py" ./sitecustomize.py
cp -f "../bundle/scripts/anti_loop_watchdog.sh" scripts/anti_loop_watchdog.sh
chmod +x scripts/anti_loop_watchdog.sh

# Merge env knobs (add-only)
if [ ! -f .env ] && [ -f .env.example ]; then
  cp -n .env.example .env || true
fi
touch .env
# Only append keys if missing
append_if_missing () {
  local key="$1"; local value="$2"
  grep -qE "^\s*${key}=" .env || printf "%s=%s\n" "$key" "$value" >> .env
}
append_if_missing "APP_DIR" "$APP_DIR"
append_if_missing "ANTI_LOOP_DB" "$HOME/ONLINPRDUCTION/var/runtime/agent_state.db"
append_if_missing "ANTI_LOOP_MAX_STEPS" "40"
append_if_missing "ANTI_LOOP_MAX_SECONDS" "900"
append_if_missing "ANTI_LOOP_DUP_WINDOW" "6"
append_if_missing "ANTI_LOOP_DUP_THRESHOLD" "3"
append_if_missing "ANTI_LOOP_TOOL_RATE" "8"
append_if_missing "ANTI_LOOP_TOOL_WINDOW" "60"
append_if_missing "ANTI_LOOP_AUTO_WRAP" "1"

# Ensure go_live_baremetal.sh respects APP_DIR default
if [ -f go_live_baremetal.sh ]; then
  cp go_live_baremetal.sh "go_live_baremetal.sh.bak.$(date +%Y%m%d_%H%M%S)"
  # Prepend default APP_DIR export if not present
  if ! grep -q 'APP_DIR=' go_live_baremetal.sh ; then
    printf '%s\n%s\n' ': "${APP_DIR:=$HOME/ONLINPRDUCTION}"' "$(cat go_live_baremetal.sh)" > go_live_baremetal.sh
  fi
fi

echo "[Anti-Loop Installer] Done. You can start your app with:"
echo "  export APP_DIR=\"$APP_DIR\""
echo "  bash ./go_live_baremetal.sh"
echo "Then open: http://localhost:8000"
echo "To check loops: ./scripts/anti_loop_watchdog.sh"
