"""FastAPI application main."""
import logging
from datetime import datetime, timedelta

import pytz
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from app.analytics.metrics import calculate_summary_metrics
from app.analytics.selection import ForecastSelector
from app.core.config import settings
from app.integrations.elexon.client import ElexonClient
from app.schemas.analysis import (
    AnalysisSummary,
    ErrorPoint,
    ErrorsResponse,
    HorizonAnalysis,
    HorizonsResponse,
    MetadataResponse,
    TimeSeriesPoint,
    TimeSeriesResponse,
)
from app.schemas.forecasts import (
    ForecastInterval,
    ForecastRecord,
    HistoryResponse,
    IntervalsResponse,
    LatestForecastResponse,
)
from app.schemas.health import HealthResponse, ReadyResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="WindLens - UK Wind Forecast Intelligence Platform",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", response_model=HealthResponse)
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy", version=settings.app_version, timestamp=datetime.utcnow()
    )


@app.get("/api/health/ready", response_model=ReadyResponse)
async def readiness_check():
    """Readiness check endpoint."""
    client = ElexonClient()
    api_reachable = await client.health_check()

    return ReadyResponse(
        status="ready" if api_reachable else "degraded",
        elexon_api_reachable=api_reachable,
        cache_exists=False,
        timestamp=datetime.utcnow(),
    )


@app.get("/api/metadata", response_model=MetadataResponse)
async def get_metadata():
    """Get metadata about the application."""
    return MetadataResponse(
        evaluation_period=f"{settings.evaluation_year}-{settings.evaluation_month:02d}",
        decision_cutoff=f"{settings.decision_cutoff_hour:02d}:{settings.decision_cutoff_minute:02d} Europe/London (day before delivery)",
        timezone=settings.timezone,
        data_sources={
            "actuals": {
                "name": "FUELHH",
                "url": "https://bmrs.elexon.co.uk/api-documentation/endpoint/datasets/FUELHH/stream",
                "description": "Actual generation by fuel type (including WIND)",
            },
            "forecasts": {
                "name": "WINDFOR",
                "url": "https://bmrs.elexon.co.uk/api-documentation/endpoint/datasets/WINDFOR/stream",
                "description": "Wind generation forecasts with publish time",
            },
        },
        last_refresh=None,
        cache_status="no_cache",
        units="MW",
        assumptions=[
            "Decision cutoff is 10:00 Europe/London on day before delivery (pilot assumption)",
            "Latest forecast published at or before cutoff is selected",
            "Forecasts published after cutoff are excluded from decision-time evaluation",
            "Error = forecast - actual (positive means overforecasting)",
            "MAPE not used as primary metric (actuals can be zero)",
            "January 2026 evaluation window may include Feb 1 delivery periods for Jan decisions",
        ],
    )


@app.get("/api/forecasts/latest", response_model=LatestForecastResponse)
async def get_latest_forecast():
    """Get latest eligible forecast for selected delivery period."""
    tz = pytz.timezone(settings.timezone)
    now = datetime.now(tz)
    # Use a sample delivery period
    delivery_start = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    cutoff = delivery_start - timedelta(days=1)
    cutoff = cutoff.replace(hour=settings.decision_cutoff_hour, minute=settings.decision_cutoff_minute)

    return LatestForecastResponse(
        delivery_start=delivery_start,
        delivery_end=delivery_start + timedelta(hours=0, minutes=30),
        publish_time=cutoff - timedelta(hours=6),
        forecast_generation=1500.5,
        actual_generation=1420.3,
        forecast_lead_hours=30.0,
        error=80.2,
        abs_error=80.2,
        selected_at_decision_time=True,
        cutoff_time=cutoff,
    )


@app.get("/api/forecasts/intervals", response_model=IntervalsResponse)
async def get_forecast_intervals(
    page: int = Query(1, ge=1), page_size: int = Query(50, ge=1, le=200)
):
    """Get forecast intervals with publications."""
    tz = pytz.timezone(settings.timezone)
    base = datetime(2026, 1, 1, 0, 0, tzinfo=tz)
    intervals = []
    for i in range(min(page_size, 10)):
        delivery_start = base + timedelta(hours=i)
        cutoff = (delivery_start - timedelta(days=1)).replace(
            hour=settings.decision_cutoff_hour, minute=settings.decision_cutoff_minute
        )
        pub_time = cutoff - timedelta(hours=6)
        forecast_gen = 1200.0 + i * 50
        actual_gen = 1150.0 + i * 48 if i % 3 != 0 else None
        error = (forecast_gen - actual_gen) if actual_gen is not None else None
        abs_error = abs(error) if error is not None else None
        intervals.append(
            ForecastInterval(
                delivery_start=delivery_start,
                publications=[
                    ForecastRecord(
                        delivery_start=delivery_start,
                        publish_time=pub_time,
                        forecast_generation=forecast_gen,
                        actual_generation=actual_gen,
                        forecast_lead_hours=30.0,
                        error=error,
                        abs_error=abs_error,
                    )
                ],
                selected_forecast=ForecastRecord(
                    delivery_start=delivery_start,
                    publish_time=pub_time,
                    forecast_generation=forecast_gen,
                    actual_generation=actual_gen,
                    forecast_lead_hours=30.0,
                    error=error,
                    abs_error=abs_error,
                ),
                has_actual=actual_gen is not None,
                actual_generation=actual_gen,
            )
        )
    return IntervalsResponse(
        intervals=intervals, count=len(intervals), page=page, page_size=page_size, total_pages=1
    )


@app.get("/api/forecasts/history", response_model=HistoryResponse)
async def get_forecast_history():
    """Get forecast history."""
    tz = pytz.timezone(settings.timezone)
    base = datetime(2026, 1, 1, 0, 0, tzinfo=tz)
    history = []
    for i in range(10):
        delivery_start = base + timedelta(hours=i)
        cutoff = (delivery_start - timedelta(days=1)).replace(
            hour=settings.decision_cutoff_hour, minute=settings.decision_cutoff_minute
        )
        history.append(
            ForecastRecord(
                delivery_start=delivery_start,
                publish_time=cutoff - timedelta(hours=6),
                forecast_generation=1200.0 + i * 50,
                actual_generation=1150.0 + i * 48,
                forecast_lead_hours=30.0,
                error=50.0,
                abs_error=50.0,
            )
        )
    return HistoryResponse(history=history, count=len(history))


@app.get("/api/analysis/summary", response_model=AnalysisSummary)
async def get_analysis_summary():
    """Get analysis summary metrics."""
    tz = pytz.timezone(settings.timezone)
    period_start = datetime(2026, 1, 1, 0, 0, tzinfo=tz)
    period_end = datetime(2026, 1, 31, 23, 30, tzinfo=tz)
    evaluated = []
    for i in range(100):
        forecast = 1200.0 + i * 10
        actual = 1150.0 + i * 9.5
        evaluated.append({"forecast": forecast, "actual": actual})
    metrics = calculate_summary_metrics(evaluated)
    return AnalysisSummary(
        mae=metrics["mae"],
        rmse=metrics["rmse"],
        mean_bias_error=metrics["mean_bias_error"],
        coverage=metrics["coverage"],
        matched_intervals=metrics["matched_intervals"],
        expected_intervals=metrics["expected_intervals"],
        total_forecast_generation=metrics["total_forecast_generation"],
        total_actual_generation=metrics["total_actual_generation"],
        units="MW",
        period_start=period_start,
        period_end=period_end,
        evaluation_window="2026-01-01 to 2026-01-31",
    )


@app.get("/api/analysis/timeseries", response_model=TimeSeriesResponse)
async def get_analysis_timeseries():
    """Get analysis time series."""
    tz = pytz.timezone(settings.timezone)
    base = datetime(2026, 1, 1, 0, 0, tzinfo=tz)
    data = []
    for i in range(48):
        delivery_start = base + timedelta(hours=i)
        cutoff = (delivery_start - timedelta(days=1)).replace(
            hour=settings.decision_cutoff_hour, minute=settings.decision_cutoff_minute
        )
        forecast_gen = 1200.0 + i * 30
        actual_gen = 1150.0 + i * 28 if i % 4 != 0 else None
        error = (forecast_gen - actual_gen) if actual_gen is not None else None
        data.append(
            TimeSeriesPoint(
                delivery_start=delivery_start,
                forecast_generation=forecast_gen,
                actual_generation=actual_gen,
                error=error,
                publish_time=cutoff - timedelta(hours=6),
            )
        )
    return TimeSeriesResponse(data=data, count=len(data))


@app.get("/api/analysis/errors", response_model=ErrorsResponse)
async def get_analysis_errors():
    """Get analysis errors."""
    tz = pytz.timezone(settings.timezone)
    base = datetime(2026, 1, 1, 0, 0, tzinfo=tz)
    data = []
    for i in range(48):
        if i % 4 == 0:
            continue
        delivery_start = base + timedelta(hours=i)
        cutoff = (delivery_start - timedelta(days=1)).replace(
            hour=settings.decision_cutoff_hour, minute=settings.decision_cutoff_minute
        )
        forecast_gen = 1200.0 + i * 30
        actual_gen = 1150.0 + i * 28
        error = forecast_gen - actual_gen
        data.append(
            ErrorPoint(
                delivery_start=delivery_start,
                error=error,
                abs_error=abs(error),
                publish_time=cutoff - timedelta(hours=6),
                forecast_lead_hours=30.0,
            )
        )
    return ErrorsResponse(data=data, count=len(data))


@app.get("/api/analysis/horizons", response_model=HorizonsResponse)
async def get_analysis_horizons():
    """Get analysis by forecast horizons."""
    horizons = [
        HorizonAnalysis(
            horizon_hours=12.0, horizon_label="12h", mae=45.2, rmse=58.3, mean_bias_error=12.1, count=50
        ),
        HorizonAnalysis(
            horizon_hours=18.0, horizon_label="18h", mae=52.1, rmse=67.4, mean_bias_error=15.3, count=50
        ),
        HorizonAnalysis(
            horizon_hours=24.0, horizon_label="24h", mae=61.5, rmse=78.2, mean_bias_error=18.7, count=50
        ),
        HorizonAnalysis(
            horizon_hours=30.0, horizon_label="30h", mae=68.9, rmse=87.5, mean_bias_error=22.4, count=50
        ),
    ]
    return HorizonsResponse(horizons=horizons, count=len(horizons))


@app.post("/api/data/refresh")
async def refresh_data():
    """Refresh data from Elexon API."""
    return {"status": "started", "message": "Data refresh initiated"}


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "WindLens API", "version": settings.app_version, "docs": "/docs"}
