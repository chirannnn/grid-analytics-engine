"""Analysis schemas."""
from datetime import datetime

from pydantic import BaseModel


class AnalysisSummary(BaseModel):
    """Analysis summary metrics."""
    mae: float
    rmse: float
    mean_bias_error: float
    coverage: float
    matched_intervals: int
    expected_intervals: int
    total_forecast_generation: float
    total_actual_generation: float
    units: str = "MW"
    period_start: datetime
    period_end: datetime
    evaluation_window: str


class TimeSeriesPoint(BaseModel):
    """Time series data point."""
    delivery_start: datetime
    forecast_generation: float
    actual_generation: float | None = None
    error: float | None = None
    publish_time: datetime


class TimeSeriesResponse(BaseModel):
    """Time series response."""
    data: list[TimeSeriesPoint]
    count: int


class ErrorPoint(BaseModel):
    """Error data point."""
    delivery_start: datetime
    error: float
    abs_error: float
    publish_time: datetime
    forecast_lead_hours: float


class ErrorsResponse(BaseModel):
    """Errors response."""
    data: list[ErrorPoint]
    count: int


class HorizonAnalysis(BaseModel):
    """Analysis by forecast horizon."""
    horizon_hours: float
    horizon_label: str
    mae: float
    rmse: float
    mean_bias_error: float
    count: int


class HorizonsResponse(BaseModel):
    """Horizons response."""
    horizons: list[HorizonAnalysis]
    count: int


class MetadataResponse(BaseModel):
    """Metadata response."""
    evaluation_period: str
    decision_cutoff: str
    timezone: str
    data_sources: dict
    last_refresh: datetime | None = None
    cache_status: str
    units: str = "MW"
    assumptions: list[str]
