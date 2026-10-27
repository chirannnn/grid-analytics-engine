"""Common schemas."""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ErrorResponse(BaseModel):
    """Error response."""
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
