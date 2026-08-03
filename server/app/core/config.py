from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn

class Settings(BaseSettings):
    PROJECT_NAME: str = "Aegis FleetScope"
    VERSION: str = "1.0.0"
    
    # Database settings - Default to localhost for development
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/aegis_fleetscope"

    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="ignore")

settings = Settings()
