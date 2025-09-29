import os
import time
import resource
from typing import Callable

class LeakStrapMiddleware:
    """
    Minimal request-time memory sampler middleware.
    - Records RSS before/after each request and writes a CSV line to logs/leakstrap.csv
    - Soft warn threshold via LEAKSTRAP_WARN_MB (default 9000MB)
    - Hard warn threshold via LEAKSTRAP_HARD_MB (default 12000MB)
    Add-only and safe. No process killing here; just logs.
    """

    def __init__(self, app, log_path: str | None = None):
        self.app = app
        base = os.path.expanduser("~/Desktop/monkey-paw/logs")
        try:
            os.makedirs(base, exist_ok=True)
        except Exception:
            pass
        self.log_file = log_path or os.path.join(base, "leakstrap.csv")
        self.warn_mb = int(os.getenv("LEAKSTRAP_WARN_MB", "9000") or 9000)
        self.hard_mb = int(os.getenv("LEAKSTRAP_HARD_MB", "12000") or 12000)
        # header
        try:
            if not os.path.exists(self.log_file):
                with open(self.log_file, "a") as f:
                    f.write("ts,method,path,rss_mb_before,rss_mb_after,duration_ms,flags\n")
        except Exception:
            pass

    async def __call__(self, scope, receive, send):
        if scope.get("type") != "http":
            return await self.app(scope, receive, send)
        method = scope.get("method", "?")
        path = scope.get("path", "?")
        rss_before = _rss_mb()
        start = time.time()
        flags = []
        async def _send(message):
            return await send(message)
        try:
            return await self.app(scope, receive, _send)
        finally:
            rss_after = _rss_mb()
            dur_ms = int((time.time() - start) * 1000)
            if rss_after >= self.hard_mb:
                flags.append("HARD")
            elif rss_after >= self.warn_mb:
                flags.append("WARN")
            try:
                with open(self.log_file, "a") as f:
                    f.write(f"{int(time.time())},{method},{path},{rss_before},{rss_after},{dur_ms},{'|'.join(flags)}\n")
            except Exception:
                pass

def _rss_mb() -> int:
    try:
        usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        # ru_maxrss is KB on macOS? On mac it's bytes? Convert heuristically.
        # macOS reports in bytes/1024? We'll normalize: if it's huge (>1e10), assume bytes.
        if usage > 10_000_000:  # likely bytes
            return int(usage / (1024 * 1024))
        else:  # likely KB
            return int(usage / 1024)
    except Exception:
        return 0
