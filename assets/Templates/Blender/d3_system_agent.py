# agents/system_agent.py

import threading
import time


class SystemAgent(threading.Thread):
    def __init__(self, bridge, emit_fn: None, interval=60):
        super().__init__(daemon=True)
        self.bridge = bridge
        self.emit_fn = emit_fn
        self.interval = interval
        self._stop = threading.Event()

    async def _async_collect(self):
        # Put your async work here (e.g., aiohttp, async DB, etc.)
        return {"ok": True, "ts": time.time()}

    def run(self):
        while not self._stop.is_set():
            try:
                fut = self.bridge.submit(self._async_collect())
                payload = fut.result(timeout=30)
                if self.emit_fn:
                    self.emit_fn("system_stats_update", payload)
            except Exception as e:
                print(f"[SystemAgent] health loop error: {e}")
            finally:
                self._stop.wait(self.interval)

    def stop(self, timeout=30):
        self._stop.set()
        self.join(timeout=timeout)
        print("[SystemAgent] stopped")
