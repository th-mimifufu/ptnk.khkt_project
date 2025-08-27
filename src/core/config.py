from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    MODEL_DIR: Path = Path("models")
    DATA_DIR: Path = Path("data")
    L2_THRESHOLD: float = 0.5

    class Config:
        env_file = ".env"

settings = Settings()