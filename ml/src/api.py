from fastapi import FastAPI
import joblib
import pandas as pd
from typing import List
from schemas import UserInput, PredictResult

app = FastAPI(title="Demo API ML",
              description="API nhập profile học sinh và trả về mã xét tuyển phù hợp nhất.")


@app.post("/predict", response_model=List[PredictResult], tags=["Gợi ý xét tuyển"])
def predict_major(user: UserInput):
    """
    API gợi ý mã xét tuyển (ngành/trường/phương thức) phù hợp nhất với profile học sinh.
    (Demo docs)
    """
    demo_results = [
        PredictResult(ma_xet_tuyen="QSA7140201ĐGNL", score=0.89),
        PredictResult(ma_xet_tuyen="QSA7140202ĐGNL", score=0.76),
        PredictResult(ma_xet_tuyen="QSA7140205ĐGNL", score=0.61),
    ]
    return demo_results