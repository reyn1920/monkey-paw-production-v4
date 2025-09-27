# Core Governance (TRAE.AI Base44)

## Rule‑1 Vocabulary Ban (hard ban)

Do not allow these tokens anywhere in code, config, docs, branches, or paths:

- live, Live, LIVE
- staging
- temporary
- experimental
- draft
- prototype, clone
- template
- verify

Preferred terms: use runtime, check, value, substitute, concrete, instance.

## Universal Persistence Rule (UPR)

- Never declare completion until two consecutive clean audits pass.
- If a check fails, fix and re‑audit; do not downgrade scope.
- Record each fix in a Fix Ledger (logs/fix_ledger.log).
- No regressions: a past fix cannot reappear later.

## No‑Delete Policy

- Never remove functionality; only improve or add.
- Treat items in Do‑Not‑Delete Stack as protected.

## Zero‑Cost Policy

- Only FOSS or already‑owned tools. No new fees or trials without approval.

## Naming & Paths

- Prefer the word runtime. Avoid banned tokens in any name/path.

## Workflow Defaults

- Backup‑first, additive changes, copy‑based renames, logs on every change.
