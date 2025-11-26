from typing import List, Tuple, Any
from src.services.l3.bk.constants import SUBJECT_MAP, AWARD_QG_POINTS, AWARD_ENGLISH_POINTS
from src.services.l3.schemas import HocBa
import pandas as pd
from src.core.config import logger

def get_dtbm(hoc_ba: HocBa, subject: str) -> float:
    """Tính điểm trung bình môn từ học bạ 3 năm."""
    field_name = SUBJECT_MAP.get(subject, subject.lower())
    logger.debug(f"[DTBM] subject={subject}, field_name={field_name}")

    scores = []
    for grade in [hoc_ba.grade_10, hoc_ba.grade_11, hoc_ba.grade_12]:
        score = getattr(grade, field_name, None)
        if score is not None:
            scores.append(score)

    avg = sum(scores) / len(scores) if scores else 0.0
    logger.debug(f"[DTBM] Scores={scores}, Avg={avg}")
    return avg


def calculate_to_hop_score(hoc_ba: Any, to_hop: List[str]) -> float:
    """Tính điểm tổ hợp môn."""
    logger.debug(f"[TO-HOP] calculate for={to_hop}")

    if len(to_hop) != 3:
        logger.debug("[TO-HOP] Invalid combination (not 3 subjects)")
        return 0.0

    dtbm_scores = [get_dtbm(hoc_ba, mon) for mon in to_hop]
    weighted_score = (dtbm_scores[0] * 2 + dtbm_scores[1] + dtbm_scores[2]) * 3
    final = weighted_score / 4

    logger.debug(f"[TO-HOP] Scores={dtbm_scores}, Final={final}")
    return final


def calculate_best_to_hop_score(hoc_ba: Any, to_hop_list: List[List[str]]) -> Tuple[float, List[str]]:
    """Chọn tổ hợp có điểm cao nhất."""
    logger.debug(f"[BEST-TO-HOP] Evaluating {len(to_hop_list)} combinations")

    if not to_hop_list:
        logger.debug("[BEST-TO-HOP] No combinations found")
        return 0.0, []

    best_score = 0.0
    best_to_hop = []

    for to_hop in to_hop_list:
        score = calculate_to_hop_score(hoc_ba, to_hop)
        logger.debug(f"[BEST-TO-HOP] {to_hop} -> {score}")

        if score > best_score:
            best_score = score
            best_to_hop = to_hop

    logger.info(f"[BEST-TO-HOP] Best Score={best_score}, ToHop={best_to_hop}")
    return best_score, best_to_hop


def calculate_bonus(award_qg: Any, award_english: Any, ma_nganh: str) -> float:
    """Tính điểm thưởng quốc gia + tiếng Anh."""
    logger.debug(f"[BONUS] Start: QG={award_qg}, ENG={award_english}, ma_nganh={ma_nganh}")

    bonus = 0.0

    # Nếu award_qg là list → lấy phần tử có level nhỏ nhất
    if isinstance(award_qg, list) and len(award_qg) > 0:
        valid_awards = [a for a in award_qg if hasattr(a, "level")]
        if valid_awards:
            award_qg = min(valid_awards, key=lambda a: a.level)
            logger.debug(f"[BONUS] Selected QG Award level={award_qg.level}")
        else:
            award_qg = None

    # Điểm thưởng quốc gia
    if award_qg and hasattr(award_qg, "level"):
        bonus_qg = AWARD_QG_POINTS.get(award_qg.level, 0.0)
        bonus += bonus_qg
        logger.debug(f"[BONUS] QG Level={award_qg.level}, +{bonus_qg}")

    # Tiếng Anh chỉ cho chương trình tiếng Anh
    if is_english_program(ma_nganh) and award_english:
        level = award_english.level if hasattr(award_english, 'level') else str(award_english)
        bonus_eng = AWARD_ENGLISH_POINTS.get(level, 0.0)
        bonus += bonus_eng
        logger.debug(f"[BONUS] English Level={level}, +{bonus_eng}")

    logger.info(f"[BONUS] Total Bonus={bonus}")
    return bonus


def is_english_program(ma_nganh: str) -> bool:
    """Kiểm tra có phải chương trình tiếng Anh không."""
    res = "A" in str(ma_nganh) or str(ma_nganh).endswith("A")
    logger.debug(f"[CHECK-ENG-PROGRAM] {ma_nganh} -> {res}")
    return res


def parse_to_hop_from_dataframe(df_to_hop: pd.DataFrame, ma_nganh: str) -> List[List[str]]:
    """Parse tổ hợp môn từ DataFrame."""
    logger.debug(f"[PARSE-TO-HOP] major_code={ma_nganh}")

    nganh_rows = df_to_hop[df_to_hop["major_code"] == ma_nganh]

    to_hop_list = []
    for _, row in nganh_rows.iterrows():
        to_hop_str = row["subject_combination"]
        logger.debug(f"[PARSE-TO-HOP] Raw={to_hop_str}")

        if isinstance(to_hop_str, str):
            clean_str = to_hop_str.strip("()")
            subjects = [s.strip().rstrip(")") for s in clean_str.split(",")]

            if len(subjects) == 3:
                to_hop_list.append(subjects)
                logger.debug(f"[PARSE-TO-HOP] Parsed={subjects}")

    logger.info(f"[PARSE-TO-HOP] Found {len(to_hop_list)} combinations")
    return to_hop_list