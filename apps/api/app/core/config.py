from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import secrets

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Excel Mock Interviewer API"
    DEBUG: bool = False
    
    # API
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@postgres:5432/interviewdb"
    TEST_DATABASE_URL: str = "postgresql+asyncpg://postgres:password@postgres:5432/test_interviewdb"
    
    # Redis
    REDIS_URL: str = "redis://redis:6379/0"
    REDIS_POOL_SIZE: int = 10
    
    # ChromaDB
    CHROMA_SERVER: Optional[str] = None
    CHROMA_DIR: str = "./chroma_data"
    
    # Auth
    GITHUB_CLIENT_ID: Optional[str] = None
    GITHUB_CLIENT_SECRET: Optional[str] = None
    JWT_SECRET: str = secrets.token_urlsafe(32)
    
    # LLM
    GROQ_API_KEY: Optional[str] = None
    PROMPT_VERSION: str = "v1"
    
    # TTS
    TTS_PROVIDER: str = "local"  # local, elevenlabs, gcloud
    TTS_API_KEY: Optional[str] = None
    
    # File Uploads
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
