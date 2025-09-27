# TRAE.AI + Online Runtime Upgrade Pack (v5 — Best Effort, Live, Cannot‑Fail)

- Live on your Mac (no virtual env). Visible browser for web tasks.
- Add‑only merge (keeps your current app intact).
- Deep recursive multi‑pass repair (cannot‑fail gate): normalize → lint/format → parse/compile → converge (clean x2).
- Health gate: API must pass /health checks to be considered up.
- Watch mode: optional file-watcher re-runs repair on changes.
- One‑liner installer included.

## One‑liner (use this from Terminal)
```bash
/bin/bash -c "$(cat <<'SH'
set -euo pipefail
# 1) Ask for (or auto-find) the ZIP; 2) install live; 3) open dashboard.
APP_DIR="${APP_DIR:-$HOME/online production}"
if [[ -z "${ZIP:-}" ]]; then
  # Try latest upgrade pack in Downloads
  CANDIDATE="$(ls -t "$HOME"/Downloads/TRAE_AI_OnlineProduction_UpgradePack_v5_best.zip 2>/dev/null | head -n1 || true)"
  if [[ -n "$CANDIDATE" ]]; then ZIP="$CANDIDATE"; else
    # macOS prompt to select the ZIP
    ZIP="$(/usr/bin/osascript -e 'POSIX path of (choose file with prompt "Select the Upgrade Pack ZIP" of type {"zip"})')"
  fi
fi
test -f "$ZIP" || { echo "ZIP not found: $ZIP"; exit 1; }
WORK="$HOME/Downloads/TRAE_v5_install"
rm -rf "$WORK" && mkdir -p "$WORK"
unzip -o "$ZIP" -d "$WORK" >/dev/null
export APP_DIR
cd "$WORK/TRAE_AI_OnlineRuntime_UpgradePack_v5_best"
bash go_live_baremetal.sh
open "http://localhost:8000"
SH
)"
```

If you already downloaded this ZIP from ChatGPT, just run the block above. It will prompt you to pick the file if needed.

---
