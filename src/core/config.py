from pydantic_settings import BaseSettings
from pathlib import Path
import os

class Settings(BaseSettings):
    MODEL_DIR: Path = Path("models")
    DATA_DIR: Path = Path("data")
    L2_THRESHOLD: float = 0.5

    # batch
    MAX_BATCH_CONCURRENCY: int = max(1, (os.cpu_count() or 4))  # ví dụ: 8/12 tuỳ máy
    BATCH_MAX_ITEMS: int = 1000
    class Config:
        env_file = ".env"
    
settings = Settings()