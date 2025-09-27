from __future__ import annotations
import csv, io, time, re
from dataclasses import dataclass
from typing import Dict, List, Any, Tuple
import urllib.parse, urllib.request
import json, os

# Multi-source takes priority; legacy single-source supported for compatibility
CONFIG_MULTI = os.environ.get("SHEETS_MULTI_CONFIG_PATH", "config/sheets_multi.json")
CONFIG_SINGLE = os.environ.get("SHEETS_CONFIG_PATH", "config/sheets.json")

_sheet_id_re = re.compile(r"/spreadsheets/d/([a-zA-Z0-9-_]+)")

@dataclass
class CacheEntry:
    expires_at: float
    rows: List[Dict[str, Any]]

class SourceCfg:
    def __init__(self, sheet_url: str, tabs: Dict[str, Dict[str, Any]]):
        m = _sheet_id_re.search(sheet_url)
        if not m:
            raise ValueError("Invalid Google Sheet URL. Expected /spreadsheets/d/<ID>")
        self.sheet_url = sheet_url
        self.sheet_id = m.group(1)
        self.tabs = tabs

class SheetsConfig:
    def __init__(self):
        self.sources: Dict[str, SourceCfg] = {}
        if os.path.exists(CONFIG_MULTI):
            with open(CONFIG_MULTI, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            for name, src in (cfg.get("sources", {}) or {}).items():
                url = (src or {}).get("sheet_url", "")
                tabs = (src or {}).get("tabs", {})
                try:
                    # Skip obvious placeholders
                    if not url or url.startswith("PASTE_"):
                        continue
                    self.sources[name] = SourceCfg(url, tabs)
                except Exception:
                    # Skip invalid entries to avoid crashing config endpoint
                    continue
        elif os.path.exists(CONFIG_SINGLE):
            with open(CONFIG_SINGLE, "r", encoding="utf-8") as f:
                one = json.load(f)
            url = (one or {}).get("sheet_url", "")
            tabs = (one or {}).get("tabs", {})
            try:
                if url and not url.startswith("PASTE_"):
                    self.sources["default"] = SourceCfg(url, tabs)
            except Exception:
                pass

def csv_url(sheet_id: str, tab_name: str) -> str:
    q = urllib.parse.urlencode({"tqx": "out:csv", "sheet": tab_name})
    return f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?{q}"

_cache: Dict[str, CacheEntry] = {}
_cfg = None  # lazy init

def _get_cfg() -> SheetsConfig:
    global _cfg
    if _cfg is None:
        _cfg = SheetsConfig()
    return _cfg

def fetch_tab(source: str, key: str) -> Tuple[List[Dict[str, Any]], int]:
    cfg = _get_cfg()
    sc = cfg.sources.get(source)
    if not sc:
        raise KeyError(f"Unknown source '{source}'. Available: {list(cfg.sources.keys())}")
    tab_cfg = sc.tabs.get(key)
    if not tab_cfg:
        raise KeyError(f"Unknown tab key '{key}' for source '{source}'. Available: {list(sc.tabs.keys())}")
    tab_name = tab_cfg["tab_name"]
    ttl = int(tab_cfg.get("ttl_seconds", 300))
    now = time.time()

    cache_key = f"{source}:{key}"
    ce = _cache.get(cache_key)
    if ce and ce.expires_at > now:
        return ce.rows, ttl

    url = csv_url(sc.sheet_id, tab_name)
    req = urllib.request.Request(url, headers={"User-Agent": "SheetsFetcher/1.1"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = resp.read()

    text = data.decode("utf-8", errors="replace")
    reader = csv.DictReader(io.StringIO(text))

    def norm(s: str) -> str:
        import re as _re
        return _re.sub(r"[^a-z0-9]+", "_", s.strip().lower()).strip("_")

    rows = [{norm(k): v for k, v in r.items()} for r in reader]
    _cache[cache_key] = CacheEntry(expires_at=now + ttl, rows=rows)
    return rows, ttl

def list_sources() -> Dict[str, List[str]]:
    cfg = _get_cfg()
    return {name: list(sc.tabs.keys()) for name, sc in cfg.sources.items()}
