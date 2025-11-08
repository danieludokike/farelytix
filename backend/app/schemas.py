
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime

class TrackedSearchCreate(BaseModel):
    origin: str
    destination: str
    depart_date: Optional[date] = None
    return_date: Optional[date] = None
    provider: Optional[str] = None
    passengers: int = 1
    cabin_class: Optional[str] = None

class TrackedSearchOut(TrackedSearchCreate):
    id: str
    created_at: datetime
    class Config:
        from_attributes = True

class PricePoint(BaseModel):
    ds: datetime | date
    price: float

class ForecastPoint(BaseModel):
    ds: datetime | date
    yhat: float
    yhat_lower: float
    yhat_upper: float

class PriceSeriesResponse(BaseModel):
    id: str
    currency: str = "USD"
    series: List[PricePoint]
    forecast: List[ForecastPoint] = Field(default_factory=list)
