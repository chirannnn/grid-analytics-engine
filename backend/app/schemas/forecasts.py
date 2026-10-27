"""Forecast schemas."""
from datetime import datetime

from pydantic import BaseModel


class ForecastRecord(BaseModel):
    """A forecast record."""
    delivery_start: datetime
    publish_time: datetime
    forecast_generation: float
    actual_generation: float | None = None
    forecast_lead_hours: float | None = None
    error: float | None = None
    abs_error: float | None = None


class LatestForecastResponse(BaseModel):
    """Latest eligible forecast response."""
    delivery_start: datetime
    delivery_end: datetime | None = None
    publish_time: datetime
    forecast_generation: float
    actual_generation: float | None = None
    forecast_lead_hours: float
    error: float | None = None
    abs_error: float | None = None
    selected_at_decision_time: bool = True
    cutoff_time: datetime


class ForecastInterval(BaseModel):
    """Forecast interval with all publications."""
    delivery_start: datetime
    publications: list[ForecastRecord]
    selected_forecast: ForecastRecord | None = None
    has_actual: bool = False
    actual_generation: float | None = None


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
