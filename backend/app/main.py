"""FastAPI application main."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import logging

from app.core.config import settings
from app.schemas.health import HealthResponse, ReadyResponse
from app.schemas.analysis import MetadataResponse
from app.integrations.elexon.client import ElexonClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="WindLens - UK Wind Forecast Intelligence Platform",
    docs_url="/docs",
    redoc_url="/redoc"
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
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version=settings.app_version,
        timestamp=datetime.utcnow()
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
        timestamp=datetime.utcnow()
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
                "description": "Actual generation by fuel type (including WIND)"
            },
            "forecasts": {
                "name": "WINDFOR",
                "url": "https://bmrs.elexon.co.uk/api-documentation/endpoint/datasets/WINDFOR/stream",
                "description": "Wind generation forecasts with publish time"
            }
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
            "January 2026 evaluation window may include Feb 1 delivery periods for Jan decisions"
        ]
    )


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "WindLens API",
        "version": settings.app_version,
        "docs": "/docs"
    }
