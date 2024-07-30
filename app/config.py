import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Twitter Analysis Service"
    PROJECT_VERSION: str = "1.0.0"
    TEAM_ID: str = "TeamCoolCloud"
    AWS_ACCOUNT_ID: str = "1234-0000-0001"

    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "user")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "password")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "db")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "twitter_analysis")
    DATABASE_URL: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: list = ["*"]  # In production, replace with actual origins

    class Config:
        case_sensitive = True

settings = Settings()