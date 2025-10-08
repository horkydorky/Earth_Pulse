"""
Earth Observation Visualizer Configuration Settings
Environment-based configuration with placeholder API endpoints
"""

import os
from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """Application configuration settings"""
    
    # Application
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    DEBUG: bool = Field(default=True, env="DEBUG")
    APP_NAME: str = Field(default="Earth Observation Visualizer", env="APP_NAME")
    APP_VERSION: str = Field(default="1.0.0", env="APP_VERSION")
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8000, env="PORT")
    
    # NASA Earth Observation APIs
    NASA_API_KEY: str = Field(default="your_nasa_api_key_here", env="NASA_API_KEY")
    NASA_EO_BASE_URL: str = Field(default="https://earthengine.googleapis.com/v1/", env="NASA_EO_BASE_URL")
    NASA_DISCOVERY_API: str = Field(default="https://api.nasa.gov/access/data/", env="NASA_DISCOVERY_API")
    NASA_EARTH_DATA_API: str = Field(default="https://earthengine.google.com/", env="NASA_EARTH_DATA_API")
    
    # Google Earth Engine Configuration
    GEE_PROJECT_ID: str = Field(default="your_gee_project_id", env="GEE_PROJECT_ID")
    GEE_ASSET_PATH: str = Field(default="/v1/projects/your-project/assets", env="GEE_ASSET_PATH")
    
    # Map Services APIs (Replace with real endpoints)
    CARTODB_API_KEY: str = Field(default="your_cartodb_key_here", env="CARTODB_API_KEY")
    MAPBOX_TOKEN: str = Field(default="your_mapbox_token_here", env="MAPBOX_TOKEN")
    MAPBOX_STYLE_URL: str = Field(default="mapbox://styles/mapbox/dark-v10", env="MAPBOX_STYLE_URL")
    
    # NASA Data Catalogs (Real endpoints ready for integration)
    NASA_MODIS_API: str = Field(default="https://lpdaacsvc.cr.usgs.gov/services/", env="NASA_MODIS_API")
    NASA_LANDSAT_API: str = Field(default="https://gsp.cr.usgs.gov/", env="NASA_LANDSAT_API")
    NASA_SENTINEL_API: str = Field(default="https://scihub.copernicus.eu/apihub/", env="NASA_SENTINEL_API")
    
    # Database Configuration (for future integration)
    DATABASE_URL: str = Field(default="postgresql://user:password@localhost:5432/earth_obs_db", env="DATABASE_URL")
    DATABASE_HOST: str = Field(default="localhost", env="DATABASE_HOST")
    DATABASE_PORT: int = Field(default=5432, env="DATABASE_PORT")
    DATABASE_NAME: str = Field(default="earth_obs_db", env="DATABASE_NAME")
    DATABASE_USER: str = Field(default="earth_obs_user", env="DATABASE_USER")
    DATABASE_PASSWORD: str = Field(default="your_db_password", env="DATABASE_PASSWORD")
    
    # Cache Configuration
    REDIS_URL: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    REDIS_HOST: str = Field(default="localhost", env="REDIS_HOST")
    REDIS_PORT: int = Field(default=6379, env="REDIS_PORT")
    
    # API Rate Limiting
    NASA_API_RATE_LIMIT: int = Field(default=1000, env="NASA_API_RATE_LIMIT")
    MAP_API_RATE_LIMIT: int = Field(default=50000, env="MAP_API_RATE_LIMIT")
    
    # File Storage
    UPLOAD_DIR: str = Field(default="./uploads", env="UPLOAD_DIR")
    REPORT_OUTPUT_DIR: str = Field(default="./reports", env="REPORT_OUTPUT_DIR")
    CACHE_DIR: str = Field(default="./cache", env="CACHE_DIR")
    MAX_FILE_SIZE: str = Field(default="100MB", env="MAX_FILE_SIZE")
    
    # Security
    SECRET_KEY: str = Field(default="your_secret_key_here_change_this_in_production", env="SECRET_KEY")
    JWT_ALGORITHM: str = Field(default="HS256", env="JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # CORS Configuration
    ALLOWED_ORIGINS: List[str] = Field(
        default=[
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:5173",
            "http://127.0.0.1:5173"
        ],
        env="ALLOWED_ORIGINS"
    )
    ALLOWED_METHODS: List[str] = Field(
        default=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        env="ALLOWED_METHODS"
    )
    ALLOWED_HEADERS: List[str] = Field(default=["*"], env="ALLOWED_HEADERS")
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FILE: str = Field(default="./logs/app.log", env="LOG_FILE")
    
    # Mock Data Configuration (Development)
    USE_MOCK_DATA: bool = Field(default=False, env="USE_MOCK_DATA")
    MOCK_DATA_REGION: str = Field(default="nepal_himalayas", env="MOCK_DATA_REGION")
    SIMULATE_API_DELAY: bool = Field(default=True, env="SIMULATE_API_DELAY")
    API_DELAY_MS: int = Field(default=500, env="API_DELAY_MS")
    
    # Environmental Data Configuration
    DATA_YEAR_MIN: int = 2000
    DATA_YEAR_MAX: int = 2025
    DEFAULT_REGION: str = "nepal_himalayas"
    
    # Supported Regions
    SUPPORTED_REGIONS: List[str] = [
        "nepal_himalayas",
        "kathmandu_valley", 
        "annapurna_region",
        "everest_region"
    ]
    
    # Supported Data Indicators
    SUPPORTED_INDICATORS: List[str] = [
        "ndvi",
        "glacier",
        "urban", 
        "temperature"
    ]
    
    # Processing Settings
    MAX_CONCURRENT_REQUESTS: int = 10
    TIMEOUT_SECONDS: int = 30
    RETRY_ATTEMPTS: int = 3
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()

# Global settings instance
settings = get_settings()
