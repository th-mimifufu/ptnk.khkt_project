from typing import List, Tuple, Any
from src.services.l3.spk.constants import SUBJECT_MAP, AWARD_QG_POINTS, AWARD_ENGLISH_POINTS
from src.services.l3.schema import HocBa
import pandas as pd

def get_dtbm(hoc_ba: HocBa, subject: str) -> float:
    """
    Tính điểm trung bình môn từ học bạ 3 năm
    
    Args:
        hoc_ba: HocBa object
        subject: Tên môn (Toán, Lý, Hóa, ...)
        
    Returns:
        Điểm trung bình môn
    """
    field_name = SUBJECT_MAP.get(subject, subject.lower())
    
    scores = []
    for grade in [hoc_ba.grade_10, hoc_ba.grade_11, hoc_ba.grade_12]:
        score = getattr(grade, field_name, None)
        if score is not None:
            scores.append(score)
    
    return sum(scores) / len(scores) if scores else 0.0

def calculate_to_hop_score(hoc_ba: Any, to_hop: List[str]) -> float:
    """
    Tính điểm cho một tổ hợp môn
    Công thức: (môn_đầu_tiên*2 + môn_thứ_hai + môn_thứ_ba) / 4
    
    Args:
        hoc_ba: HocBa object
        to_hop: List 3 môn trong tổ hợp
        
    Returns:
        Điểm tổ hợp
    """
    if len(to_hop) != 3:
        return 0.0
    
    dtbm_scores = [get_dtbm(hoc_ba, mon) for mon in to_hop]
    weighted_score = (dtbm_scores[0] * 2 + dtbm_scores[1] + dtbm_scores[2])*3
    return weighted_score / 4

def calculate_best_to_hop_score(hoc_ba: Any, to_hop_list: List[List[str]]) -> Tuple[float, List[str]]:
    """
    Tính điểm cho tất cả tổ hợp và trả về tổ hợp có điểm cao nhất
    
    Args:
        hoc_ba: HocBa object
        to_hop_list: List các tổ hợp môn. ví dụ: [['Toán', 'Lý', 'Hóa'], ['Toán', 'Anh', 'Văn'], ...]
        
    Returns:
        Tuple (điểm_cao_nhất, tổ_hợp_tốt_nhất)
    """
    if not to_hop_list:
        return 0.0, []
    
    best_score = 0.0
    best_to_hop = []
    
    for to_hop in to_hop_list:
        score = calculate_to_hop_score(hoc_ba, to_hop)
        if score > best_score:
            best_score = score
            best_to_hop = to_hop
    
    return best_score, best_to_hop

def calculate_bonus(award_qg: Any, award_english: Any, ma_nganh: str) -> float:
    """
    Tính điểm thưởng từ giải quốc gia và chứng chỉ tiếng Anh
    
    Args:
        award_qg: AwardQG object hoặc None
        award_english: AwardEnglish object hoặc None  
        ma_nganh: Mã ngành
        
    Returns:
        Tổng điểm thưởng
    """
    bonus = 0.0
    
    # Điểm thưởng quốc gia
    if award_qg and hasattr(award_qg, 'level'):
        bonus += AWARD_QG_POINTS.get(award_qg.level, 0.0)
    
    # Điểm thưởng tiếng Anh (chỉ cho chương trình tiếng Anh)
    if is_english_program(ma_nganh) and award_english:
        level = award_english.level if hasattr(award_english, 'level') else str(award_english)
        bonus += AWARD_ENGLISH_POINTS.get(level, 0.0)
    
    return bonus

def is_english_program(ma_nganh: str) -> bool:
    """Kiểm tra có phải chương trình tiếng Anh không"""
    return "A" in str(ma_nganh) or ma_nganh.endswith("A")

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
        to_hop_str = row['Tổ hợp môn']
        
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