from fastapi import APIRouter, HTTPException

from services.signals_service import SignalsService
from services.bigquery_client import BigQueryClient
from utils.logging import get_logger
from utils.db_helpers import log_error

router = APIRouter()
logger = get_logger(__name__)

@router.post("/retrain")
async def retrain_models():
    """Trigger ML model retraining or scoring via ML service."""
    try:
        result = await SignalsService().trigger_retraining()
        return {"status": "ok", "detail": result}
    except Exception as e:
        logger.exception("Retrain trigger failed")
        await log_error("admin_retrain", str(e))
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/metrics")
async def get_metrics():
    """Fetch derived metrics from BigQuery for dashboards."""
    try:
        return {"metrics": BigQueryClient().query_portfolio_metrics()}
    except Exception as e:
        logger.exception("Metrics query failed")
        await log_error("admin_metrics", str(e))
        raise HTTPException(status_code=500, detail="Internal server error")