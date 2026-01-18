from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
        
    # Application 
    app_name: str = "Personal Diet Manager"
    debug: bool = False
    environment: str = "development"  # development, production, testing
    
    # Database
    database_url: str
    database_echo: bool = False

    
    # CORS
    cors_origins: list[str] = ["http://localhost:3000"]

          
        # JWT - NOWE
    secret_key: str  # Losowy ciąg znaków do szyfrowania
    algorithm: str = "HS256"  # Algorytm szyfrowania
    access_token_expire_minutes: int = 30  # Token ważny 30 minut
    
    
@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()

