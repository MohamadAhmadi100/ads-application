import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str = f"postgresql://{os.getenv('DATABASE_USERNAME')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOST')}/{os.getenv('DATABASE_NAME')}"
    SECRET_KEY: str = os.getenv("SECRET_key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    APP_NAME: str = os.getenv("APP_NAME")
    DEBUG_MODE: bool = os.getenv("DEBUG_MODE")

    UVICORN_HOST: str = os.getenv("UVICORN_HOST")
    UVICORN_PORT: int = int(os.getenv("UVICORN_PORT", 0))


settings = Settings()
