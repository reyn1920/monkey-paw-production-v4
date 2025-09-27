"""
Monkey Paw core API — minimal health + status.
Rule-1 ready: uses "runtime" wording and avoids banned vocabulary.
"""
from fastapi import FastAPI
from pathlib import Path
import yaml

app = FastAPI(title="Monkey Paw API", version="0.1.0")

def load_features():
    cfg = Path(__file__).resolve().parents[1] / "config" / "features.yaml"
    if cfg.exists():
        try:
            return yaml.safe_load(cfg.read_text()) or {}
        except Exception:
            return {}
    return {}

@app.get("/api/health")
def health():
    feats = load_features()
    return {
        "ok": True,
        "service": "monkey-paw",
        "nocode_stack_enabled": bool(feats.get("nocode_stack_enabled", False)),
    }
