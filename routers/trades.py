from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

from services.trade_executor import TradeExecutor
from utils.logging import get_logger
from utils.db_helpers import log_error

router = APIRouter()
logger = get_logger(__name__)

class TradeRequest(BaseModel):
    ticker: str = Field(...)
    action: str = Field(..., pattern="^(buy|sell)$")
    quantity: float = Field(..., gt=0)

@router.post("/")
async def execute_trade(payload: TradeRequest):
    """Execute a paper trade and auto-update cash and active positions."""
    try:
        result = await TradeExecutor().execute_trade(
            ticker=payload.ticker, action=payload.action, quantity=payload.quantity
        )
        return result
    except Exception as e:
        logger.exception("Trade execution failed")
        await log_error("trade_execute", str(e))
        raise HTTPException(status_code=500, detail="Internal server error")