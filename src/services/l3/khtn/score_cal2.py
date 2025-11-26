from typing import Dict, List

import pandas as pd

from src.services.l3.khtn.constants import SUBJECT_MAP, AWARD_QG_POINTS, AWARD_ENGLISH_POINTS
from src.services.l3.khtn.schema import AwardQG, AdmissionInputType1c, AdmissionInputType1d, AdmissionResult, CEFRLevel, HighSchoolTranscript, PriorityObject, PriorityRegion

cefr_to_english_points: Dict[str, float] = {
        "B1": 8.0,
        "B2": 8.5,
        "C1": 10.0,
        "C2": 10.0
    }

def convert_cefr_to_english_points(cert: CEFRLevel) -> float:
    """Quy đổi CEFR level sang điểm tiếng Anh (thang 10)"""
    return cefr_to_english_points.get(cert.value, 0.0)

def calculate_high_school_grade_1c(grades: HighSchoolTranscript, subject: str) -> float:
    """Tính điểm trung bình 3 năm của một môn học trong THPT"""
    field_name = SUBJECT_MAP.get(subject, subject.lower())
    scores = []

    for grade in [grades.grade_10, grades.grade_11, grades.grade_12]:
        score = getattr(grade, field_name, None)
        if score is not None:
            scores.append(score)
    
    return sum(scores) / len(scores) if scores else 0.0

def calculate_high_school_converted(grades: HighSchoolTranscript, subject_combination: List[str]) -> float:
    """Tính điểm học THPT quy đổi"""
    # Lấy điểm trung bình 3 năm của các môn trong tổ hợp
    if len(subject_combination) != 3:
        return 0.0

    all_scores = [calculate_high_school_grade_1c(grades, subject) for subject in subject_combination]
    print("123499 All Scores:", all_scores)
    average = sum(all_scores) / len(all_scores) if all_scores else 0
    return average

def calculate_high_school_grade_1d(grades: HighSchoolTranscript, subject: str, english_cert: CEFRLevel) -> float:
    """Tính điểm học lực"""
    field_name = SUBJECT_MAP.get(subject, subject.lower())
    scores = []
    if subject == "Anh" and english_cert is not None:
        scores.append(convert_cefr_to_english_points(english_cert) / 10 * 10)  # Quy đổi thang 10
    else:
        for grade in [grades.grade_10, grades.grade_11, grades.grade_12]:
            score = getattr(grade, field_name, None)
            if score is not None:
                scores.append(score)
    return sum(scores) / len(scores) if scores else 0.0

def calculate_priority_points(academic_score: float,
                                priority_region: PriorityRegion, priority_object: PriorityObject, national_awards: List[AwardQG]) -> float:
    """Tính điểm ưu tiên"""
    priority_converted = (priority_region.value + priority_object.value)
    """Tính điểm cộng, lấy điểm cộng cao nhất"""
    award_points = max([AWARD_QG_POINTS.get(award.level, 0) for award in national_awards])

    total_score = academic_score + award_points + priority_converted

    if total_score < 28.0:
        return award_points + priority_converted
    else:
        factor = ((30 - total_score)/2) * award_points
        return factor + priority_converted

def calculate_type1(input_data: AdmissionInputType1, to_hop) -> AdmissionResult:
    """Tính điểm cho Đối tượng 1 (có ĐGNL)"""
    # Tính các thành phần điểm
    capability_score = calculate_capability_score_type1(
        input_data.dgnl_score)
    tnthpt_converted = calculate_tnthpt_converted(input_data.tnthpt_scores, to_hop, input_data.english_cert)
    high_school_converted = calculate_high_school_converted(input_data.high_school_grades, to_hop, input_data.english_cert)

    # Tính điểm học lực
    academic_score = calculate_academic_score(
        capability_score, tnthpt_converted, high_school_converted)
    
    # Tính điểm cộng và ưu tiên
    priority_points = calculate_priority_points(
        academic_score, input_data.priority_region, input_data.priority_object)

    # Tính điểm cuối cùng
    final_score = min(academic_score + priority_points, 100.0)
    
    return final_score
def calculate_type2(input_data: AdmissionInputType2, to_hop) -> AdmissionResult:
    """Tính điểm cho Đối tượng 2 (không có ĐGNL)"""
    # Tính các thành phần điểm
    tnthpt_converted = calculate_tnthpt_converted(input_data.tnthpt_scores, to_hop, input_data.english_cert)
    capability_score = calculate_capability_score_type2(tnthpt_converted)
    high_school_converted = calculate_high_school_converted(input_data.high_school_grades, to_hop, input_data.english_cert)
    
    # Tính điểm học lực
    academic_score = calculate_academic_score(
        capability_score, tnthpt_converted, high_school_converted)
    
    # Tính điểm cộng và ưu tiên
    priority_points = calculate_priority_points(
        academic_score, input_data.priority_region, input_data.priority_object)

    # Tính điểm cuối cùng
    final_score = min(academic_score + priority_points, 100.0)

    print("tnthpt_converted:", tnthpt_converted)
    print("capability_score:", capability_score)
    print("high_school_converted:", high_school_converted)
    print("academic_score:", academic_score)
    print("priority_points:", priority_points)
    print("final_score:", final_score)

    return final_score

def parse_to_hop_from_dataframe(df_to_hop: pd.DataFrame, ma_nganh: str) -> List[List[str]]:
    """
    Parse DataFrame tổ hợp môn thành List[List[str]]
    
    Args:
        df_to_hop: DataFrame với columns ['nganh', 'Tổ hợp môn']
        ma_nganh: Mã ngành cần lấy tổ hợp
        
    Returns:
        List[List[str]]: [["Toán", "Lý", "Hóa"], ["Toán", "Hóa", "Anh"], ...]
    """
    # Lọc các dòng cho ngành này
    nganh_rows = df_to_hop[df_to_hop['nganh'] == ma_nganh]
    
    to_hop_list = []
    
    for _, row in nganh_rows.iterrows():
        to_hop_str = row['to_hop_mon']
        
        # Parse "(Toán, Lý, Hoá)" -> ["Toán", "Lý", "Hoá"]
        if isinstance(to_hop_str, str):
            # Loại bỏ dấu ngoặc
            clean_str = to_hop_str.strip("()")
            # Split và clean whitespace
            subjects = [s.strip() for s in clean_str.split(",")]
            
            # Đảm bảo có đủ 3 môn
            if len(subjects) == 3:
                to_hop_list.append(subjects)
    
    return to_hop_list