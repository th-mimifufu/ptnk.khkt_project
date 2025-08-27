from types import SimpleNamespace
from fastapi import FastAPI, Depends
from typing import List

# from predict import l1_predict_from_input, l2_predict_from_input
# from schemas import L1PredictResult, UserInputL1
from src.services.l2.predictor import L2Predictor
from src.services.l2.schema import L2PredictResult, UserInputL2

from src.services.l1.predictor import L1Predictor
from src.services.l1.schema import L1PredictResult, UserInputL1

from src.core.config import settings

app = FastAPI(title="Demo API ML",
              description="API nhập profile học sinh và trả về mã xét tuyển phù hợp nhất.")
_state = SimpleNamespace()

def get_state():
    return _state

@app.on_event("startup")
def on_startup():
    _state.l1 = L1Predictor.load(settings.MODEL_DIR)
    _state.l2 = L2Predictor.load(settings.MODEL_DIR, settings.L2_THRESHOLD)

@app.get("/health", tags=["Health"])
def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy"}

@app.post("/predict/l1", response_model=List[L1PredictResult], tags=["Gợi ý xét tuyển"])
def predict_majorL1(user: UserInputL1, state=Depends(get_state)):
    """
    API gợi ý mã xét tuyển L1 (ngành/trường/phương thức) phù hợp nhất với profile học sinh TUYỂN THẲNG.
    
    """
    if not user.is_tinh_tp_valid:
        return []
    return state.l1.predict(user)

@app.post("/predict/l2", response_model=List[L2PredictResult], tags=["Gợi ý xét tuyển"])
def predict_L2(user: UserInputL2, state=Depends(get_state)):
    """
    API gợi ý mã xét tuyển L2 (ngành/trường/phương thức) phù hợp nhất với profile học sinh TPHT, ĐGNL, CCQT, VSAT, (HOCBA).
    
    """
    if not user.is_tinh_tp_valid:
        return []
    return state.l2.predict(user)

