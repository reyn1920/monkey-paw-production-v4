import shutil
from pathlib import Path
from ..store.db import cfg_get, cfg_set, cfg_path

def is_approved() -> bool:
    return bool(cfg_get("approve_publish", False))

def publish_staged() -> list[str]:
    staged = Path(cfg_path("paths.artifacts_staging"))
    pub = Path(cfg_path("paths.artifacts_published"))
    pub.mkdir(parents=True, exist_ok=True)
    moved = []
    for p in staged.glob("*"):
        dest = pub / p.name
        shutil.copy2(p, dest)
        moved.append(str(dest))
    return moved
