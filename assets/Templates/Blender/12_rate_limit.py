# tools/rate_limit.py
import time
import threading


class RateLimiter:
    def __init__(self, rate_per_minute: int = 20, capacity: int = 20):
        self.rate = rate_per_minute / 60.0
        self.capacity = capacity
        self.tokens = capacity
        self.lock = threading.Lock()
        self.last = time.time()

    def acquire(self):
        with self.lock:
            now = time.time()
            delta = now - self.last
            self.last = now
            self.tokens = min(self.capacity, self.tokens + delta * self.rate)
            if self.tokens < 1.0:
                sleep_for = (1.0 - self.tokens) / self.rate
                time.sleep(max(0.0, sleep_for))
                self.tokens = 0.0
            else:
                self.tokens -= 1.0
