#!/usr/bin/env bash
set -euo pipefail

# ------------------------------------------------------------
# TRAE.AI 20-Minute Capability Reel Launcher
# ------------------------------------------------------------
# Usage:
#   ./demo_reel.sh                       # 20-min reel (default channel)
#   ./demo_reel.sh -c "YOUR_CHANNEL"     # pick roadmap channel
#   ./demo_reel.sh -p                    # 1-min preview
#   ./demo_reel.sh -m 10                 # custom minutes
#   ./demo_reel.sh -o                    # open outputs when done (macOS)
#   ./demo_reel.sh -S                    # also run "Synthesize bundles v3"
#
# Env overrides:
#   DASH_URL="http://127.0.0.1:8083" CHANNEL="DEMO_CAPABILITY_REEL"
#   AVATARS='["Linly-Talker","TalkingHeads"]'
#   PRODUCE_EXAMPLES=true  FRESH=true
# ------------------------------------------------------------

DASH_URL="${DASH_URL:-http://127.0.0.1:8083}"
CHANNEL="${CHANNEL:-DEMO_CAPABILITY_REEL}"
MINUTES="${MINUTES:-20}"
PREVIEW=0
OPEN_ON_SUCCESS=0
RUN_SYNTH=0

AVATARS_JSON="${AVATARS:-[\"Linly-Talker\",\"TalkingHeads\"]}"
FRESH="${FRESH:-true}"
PRODUCE_EXAMPLES="${PRODUCE_EXAMPLES:-true}"
SEED="$(date +%s)"

have() { command -v "$1" >/dev/null 2>&1; }

usage() {
  sed -n '1,50p' "$0" | sed -n '5,35p'
  exit 0
}

while getopts ":c:m:poSh" opt; do
  case $opt in
    c) CHANNEL="$OPTARG" ;;
    m) MINUTES="$OPTARG" ;;
    p) PREVIEW=1; MINUTES=1 ;;
    o) OPEN_ON_SUCCESS=1 ;;
    S) RUN_SYNTH=1 ;;
    h) usage ;;
    \?) echo "Unknown option: -$OPTARG" >&2; usage ;;
  esac
done

echo "🎬 TRAE.AI Demo Reel"
echo "• Dashboard: ${DASH_URL}"
echo "• Channel:   ${CHANNEL}"
echo "• Minutes:   ${MINUTES}"
echo "• Avatars:   ${AVATARS_JSON}"
echo "• Fresh:     ${FRESH}  • Examples: ${PRODUCE_EXAMPLES}"
echo

# --- jq check (optional but nicer output)
if ! have jq; then
  echo "ℹ️  jq not found; output will be raw JSON. Install with: brew install jq" >&2
fi

# --- 1) Ensure actions manifest is loaded
echo "🔄 Reloading actions manifest..."
curl -s -X POST "${DASH_URL}/api/action/reload_actions/reload_actions" \
     -H 'Content-Type: application/json' -d '{}' >/dev/null || true

# --- 2) Verify that Run one channel exists
echo "🔎 Verifying 'Run one channel' action..."
ACTIONS_JSON="$(curl -s "${DASH_URL}/api/actions")"
if have jq; then
  RUN_EXISTS="$(printf '%s' "$ACTIONS_JSON" \
    | jq -r '.actions[]? | select(.name=="Run one channel" and .agent=="maxout") | .endpoint' | head -n1)"
else
  RUN_EXISTS="$(printf '%s' "$ACTIONS_JSON" | grep -o '/api/action/maxout/Run one channel' || true)"
fi
if [ -z "${RUN_EXISTS}" ]; then
  echo "❌ 'Run one channel' not available. Actions were:" >&2
  if have jq; then printf '%s' "$ACTIONS_JSON" | jq -r '.actions[]?.name'; else printf '%s\n' "$ACTIONS_JSON"; fi
  exit 1
fi
echo "✅ Action available."

# --- 3) (Optional) Synthesize bundles v3 to prime incoming artifacts
if [ "$RUN_SYNTH" -eq 1 ]; then
  echo "📦 Synthesize bundles v3..."
  RESP_SYNTH="$(curl -s -X POST "${DASH_URL}/api/action/maxout/Synthesize%20bundles%20v3" \
                    -H 'Content-Type: application/json' -d '{}')"
  if have jq; then printf '%s\n' "$RESP_SYNTH" | jq .; else printf '%s\n' "$RESP_SYNTH"; fi
fi

# --- 4) Kick the 20-minute capability reel (fresh seed each press)
echo "🚀 Launching capability reel..."
PAYLOAD=$(cat <<JSON
{
  "channel": "${CHANNEL}",
  "minutes": ${MINUTES},
  "fresh": ${FRESH},
  "random_seed": ${SEED},
  "avatars": ${AVATARS_JSON},
  "produce_examples": ${PRODUCE_EXAMPLES}
}
JSON
)

RESP_RUN="$(curl -s -X POST "${DASH_URL}/api/action/maxout/Run%20one%20channel" \
               -H 'Content-Type: application/json' -d "$PAYLOAD")"

echo "📨 API response:"
if have jq; then
  printf '%s\n' "$RESP_RUN" | jq .
else
  printf '%s\n' "$RESP_RUN"
fi

# --- 5) Try to extract artifacts (mp4/pdf/out dir) from various shapes
get_json_val() {
  # $1=JSON $2=jq expr (safe)
  if have jq; then
    printf '%s' "$1" | jq -r "$2 // empty" 2>/dev/null || true
  else
    echo ""
  fi
}

MP4="$(get_json_val "$RESP_RUN" '.mp4 // .video // .artifacts.mp4 // .outputs.mp4')"
PDF="$(get_json_val "$RESP_RUN" '.pdf // .ebook // .artifacts.pdf // .outputs.pdf')"
OUTDIR="$(get_json_val "$RESP_RUN" '.out_dir // .artifacts_dir // .outputs.dir')"

echo
echo "📁 Outputs (if provided):"
echo "• out_dir: ${OUTDIR:-<not reported>}"
echo "• mp4:     ${MP4:-<not reported>}"
echo "• pdf:     ${PDF:-<not reported>}"

# --- 6) Optionally open results on macOS
if [ "$OPEN_ON_SUCCESS" -eq 1 ]; then
  if [[ "$OSTYPE" == "darwin"* ]]; then
    if [ -n "${MP4:-}" ] && [ -f "$MP4" ]; then open "$MP4"; fi
    if [ -n "${PDF:-}" ] && [ -f "$PDF" ]; then open "$PDF"; fi
    if [ -z "${MP4:-}" ] && [ -z "${PDF:-}" ] && [ -n "${OUTDIR:-}" ] && [ -d "$OUTDIR" ]; then
      open "$OUTDIR"
    fi
  fi
fi

echo
echo "✅ Done."
