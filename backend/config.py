from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    """Application settings with Pydantic v2"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Database
    database_url: str | None = None
    
    # Security
    secret_key: str | None = None
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Application
    app_name: str = "Personal Diet Manager"
    debug: bool = False
    
    # CORS
    cors_origins: list[str] = ["http://localhost:3000"]

settings = Settings()

