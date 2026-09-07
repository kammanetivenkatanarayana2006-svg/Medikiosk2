from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import List, Optional
from functools import lru_cache
from enum import Enum
import os
from dotenv import load_dotenv

# Load environment variables based on APP_ENV
env_file = ".env"
app_env = os.getenv("APP_ENV", "development")
if app_env != "development":
    env_file = f".env.{app_env}"

load_dotenv(env_file)

class AppEnvironment(str, Enum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"

class Settings(BaseSettings):
    """
    Centralized application settings.
    All configuration values are loaded from environment variables.
    """
    
    # Application (ఇక్కడ lowercase aliases యాడ్ చేశాను, దీనివల్ల ఎర్రర్ హ్యాండ్లర్ కి app_name, debug దొరుకుతాయి)
    APP_NAME: str = Field(default="MediKiosk Backend", validation_alias="APP_NAME", serialization_alias="app_name")
    APP_VERSION: str = "0.1.0"
    APP_ENV: AppEnvironment = AppEnvironment.DEVELOPMENT
    DEBUG: bool = Field(default=True, validation_alias="DEBUG", serialization_alias="debug")
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database
    MONGODB_URI: Optional[str] = None
    DATABASE_NAME: str = "medikiosk"
    
    # Security (Future phases)
    JWT_SECRET: Optional[str] = None
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_ISSUER: Optional[str] = None
    JWT_AUDIENCE: Optional[str] = None
    
    # AI Services (Future phases)
    OLLAMA_BASE_URL: Optional[str] = None
    OLLAMA_MODEL: Optional[str] = None
    SARVAM_API_KEY: Optional[str] = None
    TTS_PROVIDER: Optional[str] = None
    TTS_API_KEY: Optional[str] = None
    OCR_PROVIDER: Optional[str] = None
    OCR_API_KEY: Optional[str] = None
    
    # Email (Future phases)
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: Optional[int] = 587
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAIL_FROM: Optional[str] = None
    EMAIL_USE_TLS: bool = True
    
    # WhatsApp (Future phases)
    WHATSAPP_API_URL: Optional[str] = None
    WHATSAPP_API_KEY: Optional[str] = None
    WHATSAPP_PHONE_NUMBER_ID: Optional[str] = None
    
    # SMS (Future phases)
    SMS_API_URL: Optional[str] = None
    SMS_API_KEY: Optional[str] = None
    SMS_SENDER_ID: Optional[str] = None
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    # Rate Limiting (Future)
    RATE_LIMIT_ENABLED: bool = False
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_PERIOD: int = 60  # seconds
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/medikiosk.log"
    # Sarvam ASR
    SARVAM_API_KEY: Optional[str] = None
    SARVAM_ASR_URL: str = "https://api.sarvam.ai/speech-to-text"
    SARVAM_TTS_URL: str = "https://api.sarvam.ai/text-to-speech"
    SARVAM_ASR_ENABLED: bool = True
    
    # TTS
    TTS_PROVIDER: Optional[str] = None
    TTS_ENABLED: bool = False
    TTS_API_KEY: Optional[str] = None
    #ollama
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "qwen3:1.7b"
    OLLAMA_ENABLED: bool = True
    OLLAMA_TIMEOUT_SECONDS: int = 60
    
    MAX_FOLLOWUPS_PER_INTERVIEW: int = 10
    
    model_config = SettingsConfigDict(
        env_file=env_file,
        case_sensitive=False,
        use_enum_values=True,
        extra="allow"
    )
    
    # ఈ కింద ఉన్న __getattr__ కోడ్ వల్ల చిన్న అక్షరాలతో (app_name, debug) పిలిచినా ఆటోమేటిక్‌గా Capital fields కి మ్యాప్ అవుతుంది
    def __getattr__(self, item: str):
        upper_item = item.upper()
        if upper_item in self.__dict__:
            return self.__dict__[upper_item]
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{item}'")
    
    @property
    def is_development(self) -> bool:
        return self.APP_ENV == AppEnvironment.DEVELOPMENT
    
    @property
    def is_testing(self) -> bool:
        return self.APP_ENV == AppEnvironment.TESTING
    
    @property
    def is_production(self) -> bool:
        return self.APP_ENV == AppEnvironment.PRODUCTION
    
    @property
    def database_enabled(self) -> bool:
        """Check if database is configured"""
        return bool(self.MONGODB_URI)
    
    @property
    def ai_services_enabled(self) -> bool:
        """Check if AI services are configured"""
        return bool(self.OLLAMA_BASE_URL or self.SARVAM_API_KEY)

@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Using lru_cache ensures settings are loaded only once.
    """
    return Settings()

settings = get_settings()