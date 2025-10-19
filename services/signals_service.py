import os
import httpx
from typing import Optional

ML_SERVICE_BASE = os.getenv("ML_SERVICE_BASE", "http://ml:8080")

class SignalsService:
    async def fetch_signals(self, ticker: Optional[str], lookback_days: int = 7):
        params: dict = {"lookback_days": lookback_days}
        if ticker:
            params["ticker"] = str(ticker)
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(f"{ML_SERVICE_BASE}/signals", params=params)
            resp.raise_for_status()
            return resp.json()

    async def trigger_retraining(self):
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(f"{ML_SERVICE_BASE}/admin/retrain")
            resp.raise_for_status()
            return resp.json()