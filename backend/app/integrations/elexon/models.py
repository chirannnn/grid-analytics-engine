"""Elexon API response models."""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class FuelHHRecord(BaseModel):
    """FUELHH (actual generation) record."""
    dataset: str
    startTime: datetime
    settlementDate: str
    settlementPeriod: int
    fuelType: str
    generation: float


class WindForRecord(BaseModel):
    """WINDFOR (forecast generation) record."""
    dataset: str
    startTime: datetime
    publishTime: datetime
    settlementDate: str
    settlementPeriod: int
    generation: float
    borderFrom: Optional[str] = None
    borderTo: Optional[str] = None
    scenario: Optional[str] = None


class ElexonResponse(BaseModel):
    """Generic Elexon API response."""
    data: list[dict]
    metadata: Optional[dict] = None
