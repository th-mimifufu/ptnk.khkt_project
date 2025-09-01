from fastapi import FastAPI
from types import SimpleNamespace
from src.core.config import settings
from src.services.l1.predictor import L1Predictor
from src.services.l2.predictor import L2Predictor
from src.api.routers import l1 as l1_router, l2 as l2_router, health as health_router

app = FastAPI(title="API", version="1.0.0")
_state = SimpleNamespace()

def get_state():
    return _state

@app.on_event("startup")
def on_startup():
    app.state.l1 = L1Predictor.load(settings.MODEL_DIR)
    app.state.l2 = L2Predictor.load(settings.MODEL_DIR, settings.L2_THRESHOLD)

app.include_router(health_router.router)
app.include_router(l1_router.router)
app.include_router(l2_router.router)
