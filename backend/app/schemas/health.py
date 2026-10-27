"""Health check schemas."""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    timestamp: datetime


class ReadyResponse(BaseModel):
    """Readiness check response."""
    status: str
    elexon_api_reachable: bool
    cache_exists: bool
    timestamp: datetime
