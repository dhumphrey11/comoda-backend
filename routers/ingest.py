from datetime import datetime
from typing import Optional, List

from fastapi import APIRouter, HTTPException, Query

from services.coinapi_client import CoinAPIClient
from services.santiment_client import SantimentClient
from services.yahoo_client import YahooClient
from utils.logging import get_logger
from utils.db_helpers import log_error

router = APIRouter()
logger = get_logger(__name__)

@router.get("/")
async def list_ingestions(
    ticker: Optional[str] = Query(None, description="Token ticker/symbol"),
    start_date: Optional[datetime] = Query(None, description="Start date (ISO8601)"),
    end_date: Optional[datetime] = Query(None, description="End date (ISO8601)"),
    universe: Optional[str] = Query(None, description="Token universe: portfolio|watchlist|market"),
    sources: Optional[List[str]] = Query(None, description="Data sources: coinapi|santiment|yahoo"),
):
    """
    List latest live data ingestions for tokens. Historical backfill is handled elsewhere.
    Supports filtering by ticker, date range, universe, and sources.
    """
    try:
        # Placeholder: fetch from Cloud SQL tables (ingestion logs or latest records)
        return {
            "ticker": ticker,
            "start_date": start_date,
            "end_date": end_date,
            "universe": universe,
            "sources": sources,
        }
    except Exception as e:
        logger.exception("Failed to list ingestions")
        await log_error("ingest_list", str(e))
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/")
async def create_ingestion(
    ticker: str = Query(..., description="Token ticker/symbol"),
    universe: Optional[str] = Query("market", description="Token universe: portfolio|watchlist|market"),
    sources: Optional[List[str]] = Query(default=None, description="Data sources to pull"),
):
    """Trigger live data ingestion from selected sources. No historical backfill here."""
    try:
        results = {}
        selected = sources or ["coinapi"]
        if "coinapi" in selected:
            results["coinapi"] = await CoinAPIClient().fetch_live_price(ticker)
        if "santiment" in selected:
            results["santiment"] = await SantimentClient().fetch_social_volume(ticker)
        if "yahoo" in selected:
            results["yahoo"] = await YahooClient().fetch_quote(ticker)
        return {"ticker": ticker, "universe": universe, "results": results}
    except Exception as e:
        logger.exception("Failed to create ingestion")
        await log_error("ingest_create", str(e))
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/")
async def update_ingestion(
    ticker: str,
    universe: Optional[str] = None,
):
    """Update ingestion configuration for a token (e.g., change universe)."""
    try:
        # Placeholder: update Cloud SQL row
        return {"ticker": ticker, "universe": universe}
    except Exception as e:
        logger.exception("Failed to update ingestion")
        await log_error("ingest_update", str(e))
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/")
async def delete_ingestion(
    ticker: str,
):
    """Remove token from ingestion universe (doesn't delete historical data)."""
    try:
        # Placeholder: delete from Cloud SQL
        return {"deleted": ticker}
    except Exception as e:
        logger.exception("Failed to delete ingestion")
        await log_error("ingest_delete", str(e))
        raise HTTPException(status_code=500, detail="Internal server error")