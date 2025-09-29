
import fnmatch, json
from pathlib import Path

RULES_PATH = Path("config/DO_NOT_DELETE.json")

def _rules():
    if RULES_PATH.exists():
        try:
            return json.loads(RULES_PATH.read_text())
        except Exception:
            return {"paths": []}
    return {"paths": []}

def protected(path: str) -> bool:
    st = str(Path(path))
    for pat in _rules().get("paths", []):
        if fnmatch.fnmatch(st, pat):
            return True
    return False

def assert_not_protected(path: str):
    if protected(path):
        raise PermissionError(f"Deletion blocked by Do-Not-Delete rules: {path}")
