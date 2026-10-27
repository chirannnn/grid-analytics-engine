"""Forecast schemas."""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ForecastRecord(BaseModel):
    """A forecast record."""
    delivery_start: datetime
    publish_time: datetime
    forecast_generation: float
    actual_generation: Optional[float] = None
    forecast_lead_hours: Optional[float] = None
    error: Optional[float] = None
    abs_error: Optional[float] = None


class LatestForecastResponse(BaseModel):
    """Latest eligible forecast response."""
    delivery_start: datetime
    delivery_end: Optional[datetime] = None
    publish_time: datetime
    forecast_generation: float
    actual_generation: Optional[float] = None
    forecast_lead_hours: float
    error: Optional[float] = None
    abs_error: Optional[float] = None
    selected_at_decision_time: bool = True
    cutoff_time: datetime


class ForecastInterval(BaseModel):
    """Forecast interval with all publications."""
    delivery_start: datetime
    publications: list[ForecastRecord]
    selected_forecast: Optional[ForecastRecord] = None
    has_actual: bool = False
    actual_generation: Optional[float] = None


class IntervalsResponse(BaseModel):
    """Response for forecast intervals."""
    intervals: list[ForecastInterval]
    count: int
    page: int = 1
    page_size: int = 50
    total_pages: int = 1


class HistoryResponse(BaseModel):
    """Response for forecast history."""
    history: list[ForecastRecord]
    count: int
