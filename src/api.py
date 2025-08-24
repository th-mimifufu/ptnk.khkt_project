from fastapi import FastAPI
from typing import List
from predict import l2_predict_from_input
from schemas import UserInputL2, L2PredictResult

app = FastAPI(title="Demo API ML",
              description="API nhập profile học sinh và trả về mã xét tuyển phù hợp nhất.")


# @app.post("/predict/l1", response_model=List[PredictResult], tags=["Gợi ý xét tuyển"])
# def predict_major(user: UserInputL2):
#     """
#     API gợi ý mã xét tuyển L1 (ngành/trường/phương thức) phù hợp nhất với profile học sinh TUYỂN THẲNG.
#     (Demo docs)
#     """
#     demo_results = [
#         PredictResult(ma_xet_tuyen="QSA7140201ĐGNL", score=0.89),
#         PredictResult(ma_xet_tuyen="QSA7140202ĐGNL", score=0.76),
#         PredictResult(ma_xet_tuyen="QSA7140205ĐGNL", score=0.61),
#     ]
#     return demo_results

@app.get("/health", tags=["Health"])
def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy"}

@app.post("/predict/l2", response_model=List[L2PredictResult], tags=["Gợi ý xét tuyển"])
def predict_major(user: UserInputL2):
    """
    API gợi ý mã xét tuyển L2 (ngành/trường/phương thức) phù hợp nhất với profile học sinh TPHT, ĐGNL, CCQT, VSAT, (HOCBA).
    (Demo docs)
    """
    results = l2_predict_from_input(user, threshold=0.5)
    return results

# @app.post("/predict/l3", response_model=List[PredictResult], tags=["Gợi ý xét tuyển"])
# def predict_major(user: UserInputL2):
#     """
#     API gợi ý mã xét tuyển L3 (ngành/trường/phương thức) phù hợp nhất với profile học sinh HOCBA.
#     (Demo docs)
#     """
#     demo_results = [
#         PredictResult(ma_xet_tuyen="QSA7140201ĐGNL", score=0.89),
#         PredictResult(ma_xet_tuyen="QSA7140202ĐGNL", score=0.76),
#         PredictResult(ma_xet_tuyen="QSA7140205ĐGNL", score=0.61),
#     ]
#     return demo_results
