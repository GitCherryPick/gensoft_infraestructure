# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    SECRET_KEY: str
    # ... resto de configuraciones
    
    class Config:
        env_file = ".env"

settings = Settings()