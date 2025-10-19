import httpx
from utils.rate_limit import MultiRateLimiter

YAHOO_BASE = "https://query1.finance.yahoo.com"

rate_limiter = MultiRateLimiter({
    "yahoo": {"rate_per_sec": 2.0, "burst": 10},  # Example limits
})

class YahooClient:
    async def fetch_quote(self, ticker: str):
        await rate_limiter.acquire("yahoo")
        url = f"{YAHOO_BASE}/v7/finance/quote?symbols={ticker}"
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            return resp.json()