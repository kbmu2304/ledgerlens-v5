from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://ledgerlens:ledgerlens_dev_password@db:5432/ledgerlens"
    
    # API
    api_title: str = "LedgerLens API"
    api_version: str = "0.5.0"
    api_description: str = "Financial Intelligence System - Detect anomalies, rank risk, explain findings"
    
    # Security
    jwt_secret: str = "your-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    
    # Environment
    environment: str = "development"
    debug: bool = True
    
    # OpenAI
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
