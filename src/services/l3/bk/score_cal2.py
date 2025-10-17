from typing import Dict, List

import pandas as pd

from src.services.l3.bk.hb import SUBJECT_MAP
from src.services.l3.bk.schema import DGNL, AdmissionInputType1, AdmissionInputType2, AdmissionResult, CEFRLevel, HighSchoolTranscript, PriorityObject, PriorityRegion, SubjectCombination, TNTHPTScores

cefr_to_english_points: Dict[str, float] = {
        "B1": 8.0,
        "B2": 8.5,
        "C1": 10.0,
        "C2": 10.0
    }

def convert_cefr_to_english_points(cert: CEFRLevel) -> float:
    """Quy đổi CEFR level sang điểm tiếng Anh (thang 10)"""
    return cefr_to_english_points.get(cert.value, 0.0)

def calculate_capability_score_type1(dgnl: DGNL) -> float:
    """Tính điểm năng lực cho Đối tượng 1"""
    math_coefficient = dgnl.math_score
    dgnl_score = (math_coefficient*2 + dgnl.language_score + dgnl.science_logic)
    return dgnl_score / 15

def calculate_capability_score_type2(tnthpt_converted: float) -> float:
    """Tính điểm năng lực cho Đối tượng 2"""
    return tnthpt_converted * 0.75

def calculate_tnthpt_converted(tnthpt: TNTHPTScores, subject_combination: List[str], eng_cer: CEFRLevel=None) -> float:
    """Tính điểm TNTHPT dựa trên tổ hợp môn.
    subject_combination: List 3 môn trong tổ hợp. Vd:["Toán", "Hóa", "Anh"]
    Công thức: (môn_đầu_tiên + môn_thứ_hai + môn_thứ_ba) / 3 * 10
    """
    if not subject_combination or len(subject_combination) < 3:
        return 0.0
    
    # Tạo dictionary mapping từ tên môn đến điểm
    subject_scores_dict = {
        tnthpt.math_score.subject_name: tnthpt.math_score.score,
        tnthpt.literature_score.subject_name: tnthpt.literature_score.score,
        tnthpt.elective_1_score.subject_name: tnthpt.elective_1_score.score,
        tnthpt.elective_2_score.subject_name: tnthpt.elective_2_score.score
    }
    print(123457, convert_cefr_to_english_points(eng_cer))
    # Lấy điểm của 3 môn trong tổ hợp
    subject_scores = []
    for subject in subject_combination:
        if subject in subject_scores_dict:
            if subject == "Anh" and eng_cer is not None:
                # Nếu có chứng chỉ tiếng Anh thì dùng điểm từ chứng chỉ
                subject_scores.append(convert_cefr_to_english_points(eng_cer))
            else:
                subject_scores.append(subject_scores_dict[subject])
    
    if len(subject_scores) < 3:
        return 0.0
    print("12344 Subject Scores:", subject_scores)
    total_score = sum(subject_scores)
    return (total_score / 3) * 10

def calculate_high_school_grade(grades: HighSchoolTranscript, subject: str, eng_cer: CEFRLevel=None) -> float:
    """Tính điểm trung bình 3 năm của một môn học trong THPT"""
    field_name = SUBJECT_MAP.get(subject, subject.lower())
    scores = []
    if field_name == "anh" and eng_cer is not None:
        # Nếu là môn Anh và có chứng chỉ thì dùng điểm quy đổi cho cả 3 năm
        scores = [convert_cefr_to_english_points(eng_cer)] * 3
        print(11111, scores)
    else:
        for grade in [grades.grade_10, grades.grade_11, grades.grade_12]:
            score = getattr(grade, field_name, None)
            if score is not None:
                scores.append(score)
    
    return sum(scores) / len(scores) if scores else 0.0

def calculate_high_school_converted(grades: HighSchoolTranscript, subject_combination: List[str], eng_cer: CEFRLevel=None) -> float:
    """Tính điểm học THPT quy đổi"""
    # Lấy điểm trung bình 3 năm của các môn trong tổ hợp
    if len(subject_combination) != 3:
        return 0.0

    all_scores = [calculate_high_school_grade(grades, subject, eng_cer) for subject in subject_combination]
    print("123499 All Scores:", all_scores)
    average = sum(all_scores) / len(all_scores) if all_scores else 0
    return average * 10

def calculate_academic_score(capability_score: float, tnthpt_converted: float, 
                               high_school_converted: float) -> float:
    """Tính điểm học lực"""
    return (capability_score * 0.7 + 
            tnthpt_converted * 0.2 + 
            high_school_converted * 0.1)

def calculate_priority_points(academic_score: float,
                                priority_region: PriorityRegion, priority_object: PriorityObject) -> float:
    """Tính điểm ưu tiên"""
    priority_converted = ((priority_region.value + priority_object.value) / 3) * 10
    total_before_priority = academic_score

    if total_before_priority < 75:
        return priority_converted
    else:
        factor = (100 - total_before_priority) / 25
        return round(factor * priority_converted, 2)

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