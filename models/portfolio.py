from typing import Optional, Dict
from pydantic import BaseModel, Field

class Portfolio(BaseModel):
    id: Optional[int] = None
    cash_available: float = Field(20000, ge=0)
    positions: Dict[str, float] = Field(default_factory=dict)  # ticker -> quantity
    rules: Dict[str, float] = Field(default_factory=lambda: {
        "max_allocation_pct": 5.0,
        "slippage_pct": 0.1,
        "fees_pct": 0.05,
    })