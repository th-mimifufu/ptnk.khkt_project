from enum import Enum
from typing import Dict, List

import pandas as pd

from src.services.l3.bk.hb import SUBJECT_MAP
from src.services.l3.schemas import DGNL, AwardQG, PriorityObject, PriorityRegion, TNTHPTScores, HocBa
from src.services.l3.bk.schema import AdmissionInputType1, AdmissionInputType2, AdmissionResult, CEFRLevel
from src.core.config import logger

cefr_to_english_points: Dict[str, float] = {
    "B1": 8.0,
    "B2": 8.5,
    "C1": 10.0,
    "C2": 10.0
}

def convert_cefr_to_english_points(cert: CEFRLevel) -> float:
    """Quy đổi CEFR level sang điểm tiếng Anh (thang 10)"""
    points = cefr_to_english_points.get(cert.value, 0.0)
    logger.debug(f"[CEFR] Convert {cert.value} → {points}")
    return points

def calculate_capability_score_type1(dgnl: DGNL) -> float:
    """Tính điểm năng lực cho Đối tượng 1"""
    dgnl_score = (dgnl.math_score*2 + dgnl.language_score + dgnl.science_logic)
    normalized = dgnl_score / 15
    logger.debug(f"[Type 1 Capability] Raw={dgnl_score}, Normalized={normalized}")
    return normalized

def calculate_capability_score_type2(tnthpt_converted: float) -> float:
    """Tính điểm năng lực cho Đối tượng 2"""
    score = tnthpt_converted * 0.75
    logger.debug(f"[Type 2 Capability] tnthpt_converted={tnthpt_converted}, capability={score}")
    return score

def normalize_subject_name(name: str) -> str:
    """Chuyển tên môn học về dạng chuẩn hóa."""
    SUBJECT_ALIAS = {
        "Công Nghệ Nông Nghiệp": "Công nghệ",
        "Công Nghệ Công Nghiệp": "Công nghệ",
    }
    if not name:
        return name
    normalized = SUBJECT_ALIAS.get(name.strip().title(), name.strip().title())
    logger.debug(f"[Normalize Subject] {name} → {normalized}")
    return normalized

def calculate_tnthpt_converted(tnthpt: TNTHPTScores, subject_combination: List[str], eng_cer: CEFRLevel=None) -> float:
    logger.debug(f"[TNTHPT] combination={subject_combination}, eng_cer={eng_cer}")

    subject_scores_dict = {
        tnthpt.math_score.subject_name.value if isinstance(tnthpt.math_score.subject_name, Enum)
        else tnthpt.math_score.subject_name: tnthpt.math_score.score,

        tnthpt.literature_score.subject_name.value if isinstance(tnthpt.literature_score.subject_name, Enum)
        else tnthpt.literature_score.subject_name: tnthpt.literature_score.score,

        normalize_subject_name(
            tnthpt.elective_1_score.subject_name.value if isinstance(tnthpt.elective_1_score.subject_name, Enum)
            else tnthpt.elective_1_score.subject_name
        ): tnthpt.elective_1_score.score,

        normalize_subject_name(
            tnthpt.elective_2_score.subject_name.value if isinstance(tnthpt.elective_2_score.subject_name, Enum)
            else tnthpt.elective_2_score.subject_name
        ): tnthpt.elective_2_score.score,
    }

    logger.debug(f"[TNTHPT] Subject Scores Dict: {subject_scores_dict}")

    subject_scores = []
    for subject in subject_combination:
        if subject == "Anh" and eng_cer is not None:
            eng_score = convert_cefr_to_english_points(eng_cer)
            subject_scores.append(eng_score)
            logger.debug(f"[TNTHPT] Using CEFR score for English: {eng_score}")
        else:
            score = subject_scores_dict.get(subject, 0)
            subject_scores.append(score)
            logger.debug(f"[TNTHPT] Using score {subject}: {score}")

    total_score = sum(subject_scores)
    final = (total_score / 3) * 10
    logger.debug(f"[TNTHPT] Total={total_score}, Final={final}")
    return final

def calculate_high_school_grade(grades: HocBa, subject: str, eng_cer: CEFRLevel=None) -> float:
    field_name = SUBJECT_MAP.get(subject, subject.lower())
    logger.debug(f"[HB Grade] subject={subject}, field={field_name}, eng_cer={eng_cer}")

    if field_name == "anh" and eng_cer is not None:
        point = convert_cefr_to_english_points(eng_cer)
        logger.debug(f"[HB Grade] Using CEFR for English: {point}")
        return point

    scores = []
    for grade in [grades.grade_10, grades.grade_11, grades.grade_12]:
        score = getattr(grade, field_name, None)
        if score is not None:
            scores.append(score)

    avg = sum(scores) / len(scores) if scores else 0.0
    logger.debug(f"[HB Grade] Scores={scores}, Avg={avg}")
    return avg

def calculate_high_school_converted(grades: HocBa, subject_combination: List[str], eng_cer: CEFRLevel=None) -> float:
    if len(subject_combination) != 3:
        logger.debug("[HB Converted] Invalid subject combination length")
        return 0.0

    all_scores = [calculate_high_school_grade(grades, subject, eng_cer) for subject in subject_combination]
    average = sum(all_scores) / len(all_scores) if all_scores else 0
    final = average * 10

    logger.debug(f"[HB Converted] Scores={all_scores}, Final={final}")
    return final

def calculate_academic_score(capability_score: float, tnthpt_converted: float, high_school_converted: float) -> float:
    total = (capability_score * 0.7 +
             tnthpt_converted * 0.2 +
             high_school_converted * 0.1)

    logger.debug(f"[Academic] capability={capability_score}, tnthpt={tnthpt_converted}, hb={high_school_converted}, total={total}")
    return total

def calculate_priority_points(academic_score: float,
                              priority_region: PriorityRegion, priority_object: PriorityObject) -> float:
    priority_converted = ((priority_region.value + priority_object.value) / 3) * 10
    logger.debug(f"[Priority] base_priority={priority_converted}, academic_score={academic_score}")

    if academic_score < 75:
        logger.debug(f"[Priority] No reduction, priority={priority_converted}")
        return priority_converted
    else:
        factor = (100 - academic_score) / 25
        value = round(factor * priority_converted, 2)
        logger.debug(f"[Priority] Reduced priority={value} (factor={factor})")
        return value

def calculate_type1(input_data: AdmissionInputType1, to_hop) -> AdmissionResult:
    logger.info(f"[TYPE 1] Start calculating, to_hop={to_hop}")

    capability_score = calculate_capability_score_type1(input_data.dgnl_score)
    tnthpt_converted = calculate_tnthpt_converted(input_data.tnthpt_scores, to_hop, input_data.english_cert)
    high_school_converted = calculate_high_school_converted(input_data.high_school_grades, to_hop, input_data.english_cert)

    academic_score = calculate_academic_score(capability_score, tnthpt_converted, high_school_converted)
    priority_points = calculate_priority_points(academic_score, input_data.priority_region, input_data.priority_object)

    final_score = min(academic_score + priority_points, 100.0)

    logger.info(f"[TYPE 1] Final Score={final_score}")
    return final_score

def calculate_type2(input_data: AdmissionInputType2, to_hop) -> AdmissionResult:
    logger.info(f"[TYPE 2] Start calculating, to_hop={to_hop}")

    tnthpt_converted = calculate_tnthpt_converted(input_data.tnthpt_scores, to_hop, input_data.english_cert)
    capability_score = calculate_capability_score_type2(tnthpt_converted)
    high_school_converted = calculate_high_school_converted(input_data.high_school_grades, to_hop, input_data.english_cert)

    academic_score = calculate_academic_score(capability_score, tnthpt_converted, high_school_converted)
    priority_points = calculate_priority_points(academic_score, input_data.priority_region, input_data.priority_object)

    final_score = min(academic_score + priority_points, 100.0)

    logger.info(f"[TYPE 2] Final Score={final_score}")
    return final_score

def parse_to_hop_from_dataframe(df_to_hop: pd.DataFrame, ma_nganh: str) -> List[List[str]]:
    logger.debug(f"[ParseToHop] Filtering by major_code={ma_nganh}")

    nganh_rows = df_to_hop[df_to_hop['major_code'] == ma_nganh]
    to_hop_list = []

    for _, row in nganh_rows.iterrows():
        to_hop_str = row['subject_combination']
        logger.debug(f"[ParseToHop] Raw string={to_hop_str}")

        if isinstance(to_hop_str, str):
            clean_str = to_hop_str.strip("()")
            subjects = [s.strip().rstrip(")") for s in clean_str.split(",")]
            logger.debug(f"[ParseToHop] Parsed subjects={subjects}")

            if len(subjects) == 3:
                to_hop_list.append(subjects)

    logger.debug(f"[ParseToHop] Final list={to_hop_list}")
    return to_hop_list
