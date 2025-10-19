from pydantic import BaseModel, Field
from typing import Optional

class Token(BaseModel):
    id: Optional[int] = Field(None)
    ticker: str = Field(..., min_length=1, max_length=32)
    name: Optional[str] = None
    universe: str = Field("market", pattern=r"^(portfolio|watchlist|market)$")

class TokenCreate(BaseModel):
    ticker: str
    name: Optional[str] = None
    universe: str = Field("market", pattern=r"^(portfolio|watchlist|market)$")

class TokenUpdate(BaseModel):
    name: Optional[str] = None
    universe: Optional[str] = Field(None, pattern=r"^(portfolio|watchlist|market)$")