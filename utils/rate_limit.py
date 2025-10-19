import asyncio
import time
from typing import Dict

class RateLimiter:
    """Simple token-bucket style rate limiter per key (e.g., API source)."""

    def __init__(self, rate_per_sec: float, burst: int = 1):
        self.rate_per_sec = rate_per_sec
        self.tokens = burst
        self.capacity = burst
        self.updated_at = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self):
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.updated_at
            self.updated_at = now
            self.tokens = min(self.capacity, self.tokens + elapsed * self.rate_per_sec)
            if self.tokens < 1:
                sleep_for = (1 - self.tokens) / self.rate_per_sec
                await asyncio.sleep(sleep_for)
                self.tokens = 0
            self.tokens -= 1

class MultiRateLimiter:
    """Manage multiple per-source limiters."""

    def __init__(self, configs: Dict[str, Dict[str, float]]):
        self._limiters: Dict[str, RateLimiter] = {
            name: RateLimiter(rate_per_sec=cfg.get("rate_per_sec", 1.0), burst=int(cfg.get("burst", 1)))
            for name, cfg in configs.items()
        }

    async def acquire(self, name: str):
        limiter = self._limiters.get(name)
        if limiter:
            await limiter.acquire()