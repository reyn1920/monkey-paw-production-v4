import os
from pathlib import Path
from ..store.db import DB, cfg_path, now_ts

def stage_variants(draft_id: int, variants: list[str]) -> list[str]:
    staged_dir = Path(cfg_path("paths.artifacts_staging"))
    staged_dir.mkdir(parents=True, exist_ok=True)
    outputs = []
    for v in variants:
        fname = f"draft{draft_id}_{v}_{now_ts()}.txt"
        fpath = staged_dir / fname
        fpath.write_text(f"[variant={v}] draft={draft_id} created={now_ts()}\n", encoding="utf-8")
        outputs.append(str(fpath))
    return outputs
