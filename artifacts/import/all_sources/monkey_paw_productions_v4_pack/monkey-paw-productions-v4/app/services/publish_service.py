from pathlib import Path
from shutil import copy2
from ..store.db import get_flag

BASE = Path(__file__).resolve().parents[2]
STAGING = BASE / "artifacts" / "staging"
PUBLISHED = BASE / "artifacts" / "published"

def can_publish() -> bool:
    return get_flag("approve_publish","false") == "true"

def publish_all() -> int:
    if not can_publish():
        return -1
    PUBLISHED.mkdir(parents=True, exist_ok=True)
    count = 0
    for p in STAGING.glob("*"):
        if p.is_file():
            copy2(p, PUBLISHED / p.name)
            count += 1
    return count
