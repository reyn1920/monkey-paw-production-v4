#!/bin/zsh
set -euo pipefail

# === Settings (edit if needed) ===
MONKEY="${HOME}/Desktop/monkey-paw"
ADDON="${HOME}/Desktop/nocode-coder-stack"
STAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP="${HOME}/Desktop/monkey-paw_backup_${STAMP}"
REPORT="${MONKEY}/separation_report_${STAMP}.log"

# Patterns that likely belong to the no‑code coders stack.
# Add or remove patterns as needed.
patterns=(
  "*nocode*"
  "*no-code*"
  "*lowcode*"
  "*agent*builder*"
  "*builder*agent*"
  "*workflow*builder*"
  "*wind*surf*agent*"
  "*cursor*agent*"
  "*prompt*builder*"
  "agents/nocode*"
  "prompts/nocode*"
  "tools/nocode*"
)

echo "== Monkey Paw Separator (copy-based) =="
echo "Core:   ${MONKEY}"
echo "Addon:  ${ADDON}"
echo "Backup: ${BACKUP}"
echo "Report: ${REPORT}"
echo ""

mkdir -p "${ADDON}"
mkdir -p "${BACKUP}"

# 1) Backup the current core tree (lightweight; excludes common heavy caches)
rsync -a --delete \
  --exclude ".venv" --exclude "__pycache__" --exclude ".mypy_cache" \
  --exclude ".ruff_cache" --exclude ".pytest_cache" \
  "${MONKEY}/" "${BACKUP}/"

# 2) Copy likely addon assets into the addon project (non-destructive to core)
touch "${REPORT}"
echo "Separation started: $(date)" | tee -a "${REPORT}"
echo "Patterns: ${patterns[*]}" | tee -a "${REPORT}"
echo "" | tee -a "${REPORT}"

for pat in "${patterns[@]}"; do
  matches=($(cd "${MONKEY}" && print -l **/${pat}(N)))
  if (( ${#matches[@]} > 0 )); then
    echo "Pattern '${pat}' matched ${#matches[@]} items." | tee -a "${REPORT}"
    for m in "${matches[@]}"; do
      src="${MONKEY}/${m}"
      dst="${ADDON}/${m}"
      mkdir -p "$(dirname "${dst}")"
      rsync -a "${src}" "${dst}" || true
      echo "  + copied: ${m}" | tee -a "${REPORT}"
    done
  else
    echo "Pattern '${pat}': no matches." | tee -a "${REPORT}"
  fi
done

# 3) Ensure core features toggle exists & disables the addon
mkdir -p "${MONKEY}/config"
if [[ ! -f "${MONKEY}/config/features.yaml" ]]; then
  cat > "${MONKEY}/config/features.yaml" <<'YAML'
nocode_stack_enabled: false
YAML
else
  # idempotently force false (preserve other lines)
  if grep -q "^nocode_stack_enabled:" "${MONKEY}/config/features.yaml"; then
    /usr/bin/sed -i '' 's/^nocode_stack_enabled:.*/nocode_stack_enabled: false/' "${MONKEY}/config/features.yaml"
  else
    echo "nocode_stack_enabled: false" >> "${MONKEY}/config/features.yaml"
  fi
fi

echo "" | tee -a "${REPORT}"
echo "Separation completed: $(date)" | tee -a "${REPORT}"
echo "All operations are copy-based. Original files remain in the core." | tee -a "${REPORT}"

echo ""
echo "✅ Done. Review '${REPORT}' for details."
echo "Addon tree: ${ADDON}"
echo "Backup:     ${BACKUP}"
