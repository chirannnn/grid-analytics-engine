"""Elexon API response models."""
from datetime import datetime

from pydantic import BaseModel


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
    borderFrom: str | None = None
    borderTo: str | None = None
    scenario: str | None = None


class ElexonResponse(BaseModel):
    """Generic Elexon API response."""
    data: list[dict]
    metadata: dict | None = None
