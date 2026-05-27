import os
from typing import Optional
from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

class AppSettings(BaseSettings):
    """
    App-wide settings schema using Pydantic BaseSettings.
    Validates types and presence of environment variables at startup.
    """
    # Application Mode
    APP_ENV: str = Field(default="local")

    # Security secrets
    DJANGO_SECRET: str
    FASTAPI_SECRET: str

    # Databases
    DATABASE_URL: str

    # Integrations
    OPENAI_KEY: str
    META_TOKEN: str
    META_PHONE_NUMBER_ID: str = Field(default="105581175654321")
    EMAIL_KEY: str

    model_config = SettingsConfigDict(
        # Load from .env.local if present, falling back to standard OS environment variables
        env_file=".env.local" if os.path.exists(".env.local") else ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings: Optional[AppSettings] = None

def get_settings() -> AppSettings:
    """
    Returns the validated application settings.
    Triggers validation and fails-fast on configuration errors.
    """
    global settings
    if settings is not None:
        return settings
    
    try:
        settings = AppSettings()
        return settings
    except ValidationError as e:
        print("\n" + "=" * 70)
        print("  CRITICAL ERROR: SYSTEM STARTUP BLOCKED BY VALIDATION FAILURE")
        print("=" * 70)
        print("The following environment variables are missing or invalid:")
        for error in e.errors():
            var_name = " -> ".join(str(x) for x in error["loc"])
            print(f"  - {var_name}: {error['msg']}")
        print("=" * 70 + "\n")
        raise SystemExit(1)
