from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Aegis FleetScope"
    VERSION: str = "1.0.0"
    
    # Database settings - Default to localhost for development
    DATABASE_URL: str = "postgresql://aegis:aegis_password@localhost:5432/aegis_fleetscope"

    # Security settings
    SECRET_KEY: str = "super_secret_aegis_key_for_beta"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_DAYS: int = 365
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ENROLLMENT_SECRET: str = "default_enrollment_secret"
    
    # CORS settings
    CORS_ORIGINS: list[str] = ["*"]

    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="ignore")

settings = Settings()
