from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import os
import logging

# ======================
# Settings
# ======================
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

# ======================
# Logger setup
# ======================
RESET = "\x1b[0m"
RED = "\x1b[31m"
GREEN = "\x1b[32m"
BLUE = "\x1b[34m"
YELLOW = "\x1b[33m"

class ColorFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: BLUE,
        logging.INFO: GREEN,
        logging.WARNING: YELLOW,
        logging.ERROR: RED,
        logging.CRITICAL: RED
    }

    def format(self, record):
        color = self.COLORS.get(record.levelno, RESET)
        record.levelname = f"{color}{record.levelname}{RESET}"
        return super().format(record)

# bật debug khi env APP_DEBUG=1
DEBUG_MODE = os.getenv("APP_DEBUG", "0") == "1"

logger = logging.getLogger("app_logger")
if not logger.hasHandlers():   # <-- chỉ thêm handler khi chưa có
    logger.setLevel(logging.DEBUG if DEBUG_MODE else logging.INFO)

    # Console handler với màu
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if DEBUG_MODE else logging.INFO)
    console_handler.setFormatter(ColorFormatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(console_handler)

    # File handler (ghi tất cả log, không màu)
    log_file = settings.DATA_DIR / "app.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(file_handler)

# ======================
# Example usage
# ======================
logger.info("Logger initialized (INFO green)")
logger.error("This is an error message (ERROR red)")
logger.debug("Debug message (blue, only if APP_DEBUG=1)")
logger.warning("Warning message (yellow)")
