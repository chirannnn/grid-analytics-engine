"""Application configuration."""
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""
    
    app_name: str = "WindLens API"
    app_version: str = "0.1.0"
    debug: bool = False
    
    # API settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    # Elexon BMRS API
    elexon_base_url: str = "https://data.elexon.co.uk/bmrs/api/v1"
    elexon_api_key: Optional[str] = Field(default=None, description="Optional API key if required")
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
