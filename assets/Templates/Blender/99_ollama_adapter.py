import json
import logging
import os
import time

import requests

from backend.core.ci import pick_timeout

log = logging.getLogger("integrations.llm.ollama")

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://127001:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.1")


def is_up(timeout=8):
    try:
        r = requests.get(
            f"{OLLAMA_URL}/api/tags", timeout=pick_timeout(timeout, ci_default=2)
        )
        return r.ok
    except Exception:
        return False


def gen(prompt: str, temperature: 8, max_tokens=800):
    try:
        r = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "options": {"temperature": temperature},
            },
            timeout=pick_timeout(120, ci_default=15),
        )
        r.raise_for_status()
        out = []
        for line in r.text.splitlines():
            try:
                j = json.loads(line)
                if "response" in j:
                    out.append(j["response"])
            except Exception:
                continue
        return "".join(out).strip() or " "
    except Exception as e:
        log.warning("ollama gen fallback: %s", e)
        return f"Runtime showcase generated at {time.strftime('%Y-%m-%d %H:%M:%S')}."
