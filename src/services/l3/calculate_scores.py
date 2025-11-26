import pandas as pd
from src.services.l3.schemas import L3PredictResult, UserInputL3
from src.services.l3.repository import get_all_transcript_data
from src.services.l3.spk.score_processor import process_admission_calculation as process_spk
from src.services.l3.bk.score_processor import process_admission_calculation as process_qsb
from src.core.config import logger

def calculate_scores_for_all_universities(user_input: UserInputL3, db) -> L3PredictResult:
    """
    Nhận user_input → tự động gọi cả 2 bộ tính điểm (SPK và QSB)
    """
    logger.info("Start calculating scores for all universities")
    
    df_all = get_all_transcript_data(db, user_input)
    logger.debug(f"Retrieved {len(df_all)} transcript records")

    result = {"SPK": [], "QSB": []}

    if df_all.empty:
        logger.warning("No transcript data found for user input")
        return L3PredictResult(result=result)

    # SPK
    df_spk = df_all[df_all["uni_code"] == "SPK"]
    logger.info(f"SPK: {len(df_spk)} records to process")
    if not df_spk.empty:
        try:
            result_spk = process_spk(db, user_input, df_spk, "SPK")
            if isinstance(result_spk, pd.DataFrame) and not result_spk.empty:
                result["SPK"] = result_spk.to_dict(orient="records")
                logger.info(f"SPK: calculated {len(result['SPK'])} results")
        except Exception as e:
            logger.error(f"Error calculating SPK scores: {e}", exc_info=True)

    # QSB
    df_qsb = df_all[df_all["uni_code"] == "QSB"]
    logger.info(f"QSB: {len(df_qsb)} records to process")
    if not df_qsb.empty:
        try:
            result_qsb = process_qsb(db, user_input, df_qsb, "QSB")
            if isinstance(result_qsb, pd.DataFrame) and not result_qsb.empty:
                result["QSB"] = result_qsb.to_dict(orient="records")
                logger.info(f"QSB: calculated {len(result['QSB'])} results")
        except Exception as e:
            logger.error(f"Error calculating QSB scores: {e}", exc_info=True)

    logger.info("Finished calculating scores for all universities")
    return L3PredictResult(result=result)