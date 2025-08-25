from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Pydantic automatically loads values from:
    1. Environment variables
    2. .env file
    3. Default values defined here
    """
    
    # Database settings
    database_url: str = "sqlite:///./todo_app.db"
    
    # Security settings
    secret_key: str = "your-super-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # App settings
    app_name: str = "Todo API"
    debug: bool = True
    
    class Config:
        # Tell Pydantic to load from .env file
        env_file = ".env"

# Create a global settings instance
settings = Settings()