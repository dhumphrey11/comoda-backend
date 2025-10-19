import os
import httpx
from utils.rate_limit import MultiRateLimiter

COINAPI_BASE = "https://rest.coinapi.io/v1"

rate_limiter = MultiRateLimiter({
    "coinapi": {"rate_per_sec": 1.0, "burst": 5},  # Adjust per official limits
})

class CoinAPIClient:
    def __init__(self):
        self.api_key = os.getenv("COINAPI_KEY", "")

    async def fetch_live_price(self, ticker: str):
        await rate_limiter.acquire("coinapi")
        headers = {"X-CoinAPI-Key": self.api_key}
        url = f"{COINAPI_BASE}/trades/latest?symbol_id={ticker}"
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(url, headers=headers)
            resp.raise_for_status()
            return resp.json()