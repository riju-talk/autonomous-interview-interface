from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, List, Union
import secrets
from functools import lru_cache

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Autonomous Interview API"
    DEBUG: bool = False
    
    # API
    API_V1_STR: str = "/api/v1"
    
    # Database - Use environment variable if available, fallback to SQLite for development
    DATABASE_URL: str = "sqlite+aiosqlite:///./interview.db"
    TEST_DATABASE_URL: str = "sqlite+aiosqlite:///./test_interview.db"
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_PASSWORD: Optional[str] = None
    REDIS_POOL_SIZE: int = 10
    
    # ChromaDB
    CHROMA_SERVER: Optional[str] = None
    CHROMA_DIR: str = "./chroma_data"
    CHROMA_AUTH_CREDENTIALS: Optional[str] = None
    
    # LLM
    GROQ_API_KEY: Optional[str] = None
    PROMPT_VERSION: str = "v1"
    
    # TTS
    TTS_PROVIDER: str = "local"  # local, elevenlabs, gcloud
    TTS_API_KEY: Optional[str] = None
    
    # File Uploads
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # CORS - Allow Replit frontend access
    CORS_ORIGINS: List[str] = ["*"]
    
    # Server
    HOST: str = "localhost"
    PORT: int = 8000
    WORKERS: int = 1
    RELOAD: bool = False
    
    # Rate Limiting
    RATE_LIMIT: str = "100/minute"
    
    # Logging
    LOG_LEVEL: str = "info"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Monitoring
    SENTRY_DSN: Optional[str] = None
    ENVIRONMENT: str = "development"
    TESTING: bool = False
    
    # Email
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAIL_FROM: str = "noreply@example.com"
    
    # Security
    SECURE_COOKIES: bool = False
    SESSION_COOKIE_NAME: str = "session"
    SESSION_SECRET_KEY: str = secrets.token_urlsafe(32)
    
    # Feature Flags
    ENABLE_ANALYTICS: bool = False
    ENABLE_EMAIL_VERIFICATION: bool = False
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

@lru_cache()
def get_settings() -> Settings:
    """
    Get application settings with caching.
    This function is cached to prevent reading the .env file multiple times.
    """
    return Settings()

# Global settings instance
settings = get_settings()
