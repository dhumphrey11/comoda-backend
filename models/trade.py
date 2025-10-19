from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class Trade(BaseModel):
    id: Optional[int] = None
    ticker: str
    action: str = Field(..., pattern=r"^(buy|sell)$")
    quantity: float = Field(..., gt=0)
    price: float = Field(..., gt=0)
    executed_at: datetime = Field(default_factory=datetime.utcnow)

class TradeCreate(BaseModel):
    ticker: str
    action: str = Field(..., pattern=r"^(buy|sell)$")
    quantity: float = Field(..., gt=0)

class TradeUpdate(BaseModel):
    price: Optional[float] = Field(None, gt=0)
    quantity: Optional[float] = Field(None, gt=0)