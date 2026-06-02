from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://contextmind:secret@localhost:5432/contextmind_db"
    REDIS_URL: str = "redis://localhost:6379"
    QDRANT_URL: str = "http://localhost:6333"
    GROQ_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    JWT_SECRET: str = "your-super-secret-key-change-this"
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"

settings = Settings()
