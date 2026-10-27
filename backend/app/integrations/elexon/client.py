"""Elexon BMRS API client."""
import httpx
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from tenacity import retry, stop_after_attempt, wait_exponential
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)


class ElexonClient:
    """Client for Elexon BMRS API."""
    
    def __init__(self):
        self.base_url = settings.elexon_base_url
        self.timeout = settings.elexon_timeout
        self.api_key = settings.elexon_api_key
        self.headers = {}
        if self.api_key:
            self.headers["Authorization"] = f"Bearer {self.api_key}"
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def _fetch(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Fetch data from Elexon API with retries."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            url = f"{self.base_url}/{endpoint}"
            response = await client.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            return response.json()
    
    async def get_fuelhh_wind(self, from_date: str, to_date: str) -> List[Dict[str, Any]]:
        """
        Get actual wind generation from FUELHH dataset.
        FUELHH contains half-hourly generation by fuel type.
        """
        logger.info(f"Fetching FUELHH wind data from {from_date} to {to_date}")
        try:
            # Try different parameter formats based on Elexon API conventions
            params = {
                "from": from_date,
                "to": to_date,
                "format": "json"
            }
            data = await self._fetch("datasets/FUELHH", params)
            records = data.get("data", []) if isinstance(data, dict) else data
            
            # Filter for WIND fuel type
            wind_records = []
            for rec in records:
                if isinstance(rec, dict):
                    fuel_type = rec.get("fuelType") or rec.get("fuel_type") or rec.get("FuelType")
                    if fuel_type and str(fuel_type).upper() == "WIND":
                        wind_records.append(rec)
            
            logger.info(f"Fetched {len(wind_records)} WIND records from FUELHH")
            return wind_records
        except Exception as e:
            logger.error(f"Error fetching FUELHH data: {e}")
            raise
    
    async def get_windfor(self, from_date: str, to_date: str) -> List[Dict[str, Any]]:
        """
        Get wind forecast from WINDFOR dataset.
        WINDFOR contains forecast generation with publishTime.
        """
        logger.info(f"Fetching WINDFOR data from {from_date} to {to_date}")
        try:
            params = {
                "from": from_date,
                "to": to_date,
                "format": "json"
            }
            data = await self._fetch("datasets/WINDFOR", params)
            records = data.get("data", []) if isinstance(data, dict) else data
            
            logger.info(f"Fetched {len(records)} records from WINDFOR")
            return records
        except Exception as e:
            logger.error(f"Error fetching WINDFOR data: {e}")
            raise
    
    async def health_check(self) -> bool:
        """Check if Elexon API is reachable."""
        try:
            # Try a simple request
            await self._fetch("datasets/FUELHH", {"from": "2026-01-01", "to": "2026-01-01", "format": "json"})
            return True
        except Exception as e:
            logger.error(f"Elexon API health check failed: {e}")
            return False
