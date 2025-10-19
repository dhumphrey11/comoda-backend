from typing import Optional
from fastapi import APIRouter, HTTPException, Query

from services.signals_service import SignalsService
from services.bigquery_client import BigQueryClient
from utils.logging import get_logger
from utils.db_helpers import log_error

router = APIRouter()
logger = get_logger(__name__)

@router.get("/")
async def get_signals(
    ticker: Optional[str] = Query(None),
    lookback_days: int = Query(7, ge=1, le=365),
    include_analytics: bool = Query(False, description="Also query BigQuery analytics"),
):
    """Fetch signal scores from ML service; optionally join with BigQuery analytics."""
    try:
        signals = await SignalsService().fetch_signals(ticker=ticker, lookback_days=lookback_days)
        analytics = None
        if include_analytics:
            analytics = BigQueryClient().query_signals_analytics(ticker=ticker, lookback_days=lookback_days)
        return {"signals": signals, "analytics": analytics}
    except Exception as e:
        logger.exception("Failed to fetch signals")
        await log_error("signals_get", str(e))
        raise HTTPException(status_code=500, detail="Internal server error")