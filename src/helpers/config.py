from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
     # Defining settings with Pydantic
     APP_NAME: str
     APP_VERSION: str
     OPENAI_API_KEY: str
     FILE_ALLOWED_TYPES: list
     FILE_MAX_SIZE: int
     FILE_DEFAULT_CHUNK_SIZE: int
     class Config:  # Configuration for Pydantic settings
        env_file = ".env"

def get_settings() -> Settings:
    # Function to get settings instance
    return Settings()
