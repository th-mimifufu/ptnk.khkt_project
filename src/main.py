from fastapi import FastAPI
from types import SimpleNamespace
from src.core.config import settings, logger
from src.services.l1.predictor import L1Predictor
from src.services.l2.predictor import L2Predictor
from src.api.routers import l1 as l1_router, l2 as l2_router, health as health_router, l3 as l3_router

app = FastAPI(title="API", version="1.0.0")
_state = SimpleNamespace()

def get_state():
    return _state

@app.on_event("startup")
def on_startup():
    logger.info("Starting API server, loading models...")
    try:
        app.state.l1 = L1Predictor.load(settings.MODEL_DIR)
        logger.info("L1Predictor loaded successfully")
    except Exception as e:
        logger.exception(f"Failed to load L1Predictor: {e}")

    try:
        app.state.l2 = L2Predictor.load(settings.MODEL_DIR, settings.L2_THRESHOLD)
        logger.info("L2Predictor loaded successfully")
    except Exception as e:
        logger.exception(f"Failed to load L2Predictor: {e}")

app.include_router(health_router.router)
app.include_router(l1_router.router)
app.include_router(l2_router.router)
app.include_router(l3_router.router)
logger.info("Routers registered, API ready")
