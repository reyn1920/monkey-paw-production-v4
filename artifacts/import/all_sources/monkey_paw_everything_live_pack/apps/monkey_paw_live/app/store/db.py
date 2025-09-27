from __future__ import annotations
import time, json
from pathlib import Path
import yaml

CFG_PATH = Path(__file__).resolve().parents[2] / "config" / "config.yaml"

DB = {
    "seq": {"research": 1, "draft": 1},
    "research": {},
    "draft": {},
}

def now_ts() -> str:
    return time.strftime("%Y%m%d_%H%M%S", time.gmtime())

def _read_cfg() -> dict:
    if CFG_PATH.exists():
        return yaml.safe_load(CFG_PATH.read_text(encoding="utf-8")) or {}
    return {}

def _write_cfg(data: dict) -> None:
    CFG_PATH.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

def cfg_get(key: str, default=None):
    data = _read_cfg()
    cur = data
    for part in key.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return default
    return cur

def cfg_set(key: str, value) -> None:
    data = _read_cfg()
    cur = data
    parts = key.split(".")
    for part in parts[:-1]:
        if part not in cur or not isinstance(cur[part], dict):
            cur[part] = {}
        cur = cur[part]
    cur[parts[-1]] = value
    _write_cfg(data)

def cfg_path(key: str) -> str:
    base = Path(__file__).resolve().parents[2]
    val = cfg_get(key, "")
    return str((base / val).resolve())

def approve_set(v: bool) -> None:
    cfg_set("approve_publish", bool(v))

def get_state_snapshot() -> dict:
    return {
        "service_name": cfg_get("service_name", "monkey-paw-live"),
        "flags": {"nocode_stack_enabled": cfg_get("flags.nocode_stack_enabled", False)},
        "paths": {
            "staging": cfg_get("paths.artifacts_staging", "artifacts/staging"),
            "published": cfg_get("paths.artifacts_published", "artifacts/published"),
        },
        "counts": {"research": len(DB["research"]), "draft": len(DB["draft"])},
        "approve_publish": cfg_get("approve_publish", False),
    }

def selfcheck_state() -> dict:
    st = get_state_snapshot()
    # Minimal integrity: config readable, paths strings present
    ok = isinstance(st["paths"]["staging"], str) and isinstance(st["paths"]["published"], str)
    return {"ok": bool(ok), "snapshot": st}
