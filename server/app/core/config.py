from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Aegis FleetScope"
    VERSION: str = "1.0.0"
    
    # Database settings - Default to localhost for development
    DATABASE_URL: str = "postgresql://aegis:aegis_password@localhost:5432/aegis_fleetscope"

    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="ignore")

settings = Settings()
