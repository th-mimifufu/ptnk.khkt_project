import pandas as pd
from src.services.l3.schemas import L3PredictResult, UserInputL3
from src.services.l3.repository import get_all_transcript_data
from src.services.l3.spk.score_processor import process_admission_calculation as process_spk
from src.services.l3.bk.score_processor import process_admission_calculation as process_qsb

def calculate_scores_for_all_universities(user_input: UserInputL3, db) -> L3PredictResult:
    """
    Nhận user_input → tự động gọi cả 2 bộ tính điểm (SPK và QSB)
    """
    df_all = get_all_transcript_data(db, user_input)
    result = {"SPK": [], "QSB": []}

    if df_all.empty:
        return L3PredictResult(result=result)

    # SPK
    df_spk = df_all[df_all["uni_code"] == "SPK"]
    if not df_spk.empty:
        try:
            result_spk = process_spk(db, user_input, df_spk, "SPK")
            if isinstance(result_spk, pd.DataFrame) and not result_spk.empty:
                result["SPK"] = result_spk.to_dict(orient="records")
        except Exception as e:
            print(f"[ERROR] Lỗi khi tính SPK: {e}")

    # QSB
    df_qsb = df_all[df_all["uni_code"] == "QSB"]
    if not df_qsb.empty:
        try:
            result_qsb = process_qsb(db, user_input, df_qsb, "QSB")
            if isinstance(result_qsb, pd.DataFrame) and not result_qsb.empty:
                result["QSB"] = result_qsb.to_dict(orient="records")
        except Exception as e:
            print(f"[ERROR] Lỗi khi tính QSB: {e}")

    return L3PredictResult(result=result)