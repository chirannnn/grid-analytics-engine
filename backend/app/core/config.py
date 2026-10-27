"""Application configuration."""

import json
from typing import Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    app_name: str = "WindLens API"
    app_version: str = "0.1.0"
    debug: bool = False

    # API settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000", "http://localhost:8080", "http://localhost"]

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Any) -> list[str]:
        if isinstance(v, str):
            # Try to parse as JSON first
            v_stripped = v.strip()
            if v_stripped.startswith("[") and v_stripped.endswith("]"):
                try:
                    parsed = json.loads(v_stripped)
                    if isinstance(parsed, list):
                        return parsed
                except json.JSONDecodeError:
                    pass
            # Otherwise split by comma
            if "," in v_stripped:
                return [origin.strip().strip('"').strip("'") for origin in v_stripped.split(",") if origin.strip()]
            # Single value
            return [v_stripped.strip('"').strip("'")]
        elif isinstance(v, list):
            return v
        return v

    # Elexon BMRS API
    elexon_base_url: str = "https://data.elexon.co.uk/bmrs/api/v1"
    elexon_api_key: str | None = Field(default=None, description="Optional API key if required")
    elexon_timeout: int = 30
    elexon_max_retries: int = 3

    # Data settings
    data_cache_dir: str = "./data/cache"
    decision_cutoff_hour: int = 10  # 10:00 Europe/London
    decision_cutoff_minute: int = 0
    timezone: str = "Europe/London"

    # Evaluation settings
    evaluation_year: int = 2026
    evaluation_month: int = 1

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
