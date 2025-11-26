from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.services.l3.schemas import L3PredictResult, UserInputL3
from src.services.l3.calculate_scores import calculate_scores_for_all_universities

router = APIRouter(tags=["Gợi ý xét tuyển"])

@router.post("/calculate/l3", response_model=L3PredictResult)
def calculate_scores(user_input: UserInputL3, db: Session = Depends(get_db)):
    df_result = calculate_scores_for_all_universities(user_input, db=db)
    return df_result

@router.post("/calculate/l3/batch", response_model=List[L3PredictResult])
def calculate_scores_batch(user_inputs: List[UserInputL3], db: Session = Depends(get_db)):
    """
    API batch tính điểm cho nhiều học sinh cùng lúc.
    Nhận danh sách UserInputL3 -> trả danh sách kết quả L3PredictResult tương ứng.
    """
    results = []
    for user_input in user_inputs:
        try:
            result = calculate_scores_for_all_universities(user_input, db=db)
            results.append(result)
        except Exception as e:
            print(f"[ERROR] Batch entry failed: {e}")
            results.append(L3PredictResult(__root__={"SPK": None, "QSB": None}))
    return results