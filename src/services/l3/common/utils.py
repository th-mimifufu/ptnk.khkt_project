import pandas as pd
from typing import List, Any

def parse_to_hop_from_dataframe(df_to_hop: pd.DataFrame, ma_nganh: str) -> List[List[str]]:
    """
    Parse DataFrame tổ hợp môn thành List[List[str]]
    """
    nganh_rows = df_to_hop[df_to_hop['nganh'] == ma_nganh]
    
    to_hop_list = []
    
    for _, row in nganh_rows.iterrows():
        to_hop_str = row['Tổ hợp môn']
        
        if isinstance(to_hop_str, str):
            clean_str = to_hop_str.strip("()")
            subjects = [s.strip() for s in clean_str.split(",")]
            
            if len(subjects) == 3:
                to_hop_list.append(subjects)
    
    return to_hop_list

def get_subject_score(hoc_ba: Any, nang_khieu: Any, subject: str, full_subject_map: dict) -> float:
    """
    Lấy điểm môn từ học bạ hoặc năng khiếu (nếu là môn năng khiếu)
    
    Args:
        hoc_ba: HocBa object
        nang_khieu: NangKhieu object (có thể None)
        subject: Tên môn (Toán, Lý, Hóa, Vẽ TT, Vẽ DT, ...)
        full_subject_map: Dict mapping tên môn sang field name
        
    Returns:
        Điểm trung bình môn từ học bạ 3 năm hoặc điểm năng khiếu
    """
    field_name = full_subject_map.get(subject, subject.lower())
    
    # Nếu là môn năng khiếu
    if subject in ["Vẽ TT", "Vẽ DT"] and nang_khieu:
        score = getattr(nang_khieu, field_name, None)
        return score if score is not None else 0.0
    
    # Nếu là môn học thường - tính trung bình 3 năm
    scores = []
    for grade in [hoc_ba.grade_10, hoc_ba.grade_11, hoc_ba.grade_12]:
        score = getattr(grade, field_name, None)
        if score is not None:
            scores.append(score)
    
    return sum(scores) / len(scores) if scores else 0.0

# Deprecated function - keep for backward compatibility
def get_dtbm(hoc_ba: Any, subject: str, subject_map: dict) -> float:
    """
    DEPRECATED: Sử dụng get_subject_score() thay thế
    Tính điểm trung bình môn từ học bạ 3 năm
    """
    return get_subject_score(hoc_ba, None, subject, subject_map)
