from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class Signal(BaseModel):
    id: Optional[int] = None
    ticker: Optional[str] = None
    score: float = Field(..., ge=-1.0, le=1.0)
    generated_at: datetime = Field(default_factory=datetime.utcnow)

class SignalQuery(BaseModel):
    ticker: Optional[str] = None
    lookback_days: int = Field(7, ge=1, le=365)