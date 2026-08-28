from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "AGNIV"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./agniv.db"
    
    # Environment
    ENV: str = "development" # development, production, portable
    GROQ_API_KEY: Optional[str] = None
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
