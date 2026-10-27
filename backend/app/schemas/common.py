"""Common schemas."""
from datetime import datetime

from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """Error response."""
    error: str
    detail: str | None = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
