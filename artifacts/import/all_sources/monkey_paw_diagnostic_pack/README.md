# Monkey Paw Diagnostic Pack
Run a full, read-only scan to see what the app does **now**.
Quick start:
```bash
# From your repository root:
mkdir -p ./scripts_diag
cp -a ./monkey_paw_diagnostic_pack/scripts/* ./scripts_diag/
zsh ./scripts_diag/diagnose_all.zsh .
# Reports:
ls -la ./reports
# Open the latest ./reports/diagnostic_*/SUMMARY.md
```
