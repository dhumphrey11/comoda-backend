import os
import httpx
from utils.rate_limit import MultiRateLimiter

SANTIMENT_BASE = "https://api.santiment.net"

rate_limiter = MultiRateLimiter({
    "santiment": {"rate_per_sec": 0.5, "burst": 2},  # Example limits
})

class SantimentClient:
    def __init__(self):
        self.api_key = os.getenv("SANTIMENT_API_KEY", "")

    async def fetch_social_volume(self, ticker: str):
        await rate_limiter.acquire("santiment")
        headers = {"Authorization": f"Apikey {self.api_key}"}
        url = f"{SANTIMENT_BASE}/labs/sanapi/social_volume?slug={ticker}"
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(url, headers=headers)
            resp.raise_for_status()
            return resp.json()