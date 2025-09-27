# Integration Notes

- Treat this as an optional layer. The core (monkey‑paw) should run even if this addon is absent.
- If you later want to re‑enable, flip `nocode_stack_enabled: true` in the core `config/features.yaml` and attach endpoints via an extension router.
