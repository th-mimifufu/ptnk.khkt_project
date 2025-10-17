from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import os

class Settings(BaseSettings):
    MODEL_DIR: Path
    DATA_DIR: Path 
    L2_THRESHOLD: float = 0.5
    OCR_MISTRAL: str = ""

    # batch
    MAX_BATCH_CONCURRENCY: int = max(1, (os.cpu_count() or 4))
    BATCH_MAX_ITEMS: int 

    # database
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()