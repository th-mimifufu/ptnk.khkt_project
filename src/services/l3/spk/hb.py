from typing import Dict, List, Optional, Set
import pandas as pd

from src.services.l3.schema import HocBa, Grade
AWARD_QG_POINTS = {
    1: 1.2,
    2: 1.2,
    3: 1.2,
    4: 1.0
}

AWARD_ENGLISH_POINTS = {
    "A1": 0.0,
    "A2": 0.0,
    "B1": 0.5,
    "B2": 0.8,
    "C1": 1.0,
    "C2": 1.0
}

SUBJECT_MAP = {
    "Toán": "toan", 
    "Lý": "ly", 
    "Hóa": "hoa", 
    "Văn": "van", 
    "Anh": "anh",
    "Sinh": "sinh", 
    "Sử": "su", 
    "Địa": "dia", 
    "Tin": "tin",
    "GDKT&PL": "gdkt_pl",
    "Vẽ TT": "ve_tt",
    "Vẽ DT": "ve_dt"
}

def get_dtbm(hoc_ba: HocBa, subject: str) -> float:
    """Tính điểm trung bình môn từ học bạ 3 năm"""
    field_name = SUBJECT_MAP.get(subject, subject.lower())
    
    scores = []
    # Lấy điểm từ 3 lớp
    for grade in [hoc_ba.grade_10, hoc_ba.grade_11, hoc_ba.grade_12]:
        score = getattr(grade, field_name, None)
        if score is not None:
            scores.append(score)
    
    return sum(scores) / len(scores) if scores else 0.0

def get_unique_subjects(to_hop_list: List[List[str]]) -> Set[str]:
    """Lấy tất cả môn học duy nhất từ danh sách các tổ hợp"""
    unique_subjects = set()
    for to_hop in to_hop_list:
        unique_subjects.update(to_hop)
    return unique_subjects

def calculate_to_hop_score(hoc_ba: HocBa, to_hop: List[str]) -> float:
    """
    Tính điểm cho một tổ hợp môn
    Công thức: (môn_đầu_tiên*2 + môn_thứ_hai + môn_thứ_ba) / 4
    """
    if len(to_hop) != 3:
        return 0.0
    
    dtbm_scores = [get_dtbm(hoc_ba, mon) for mon in to_hop]
    
    # Môn đầu tiên nhân 2, các môn khác nhân 1
    weighted_score = dtbm_scores[0] * 2 + dtbm_scores[1] + dtbm_scores[2]
    return weighted_score / 4

def calculate_best_to_hop_score(hoc_ba: HocBa, to_hop_list: List[List[str]]) -> tuple[float, List[str]]:
    """
    Tính điểm cho tất cả tổ hợp và trả về tổ hợp có điểm cao nhất
    
    Returns:
        tuple: (điểm_cao_nhất, tổ_hợp_tốt_nhất)
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

def calculate_bonus(award_qg: Optional[Dict], award_english: Optional[str], ma_nganh: str) -> float:
    """Tính điểm thưởng"""
    bonus = 0.0
    
    # Điểm thưởng quốc gia
    if isinstance(award_qg, dict) and "level" in award_qg:
        bonus += AWARD_QG_POINTS.get(award_qg["level"], 0.0)
    
    # Điểm thưởng tiếng Anh (chỉ cho chương trình tiếng Anh)
    if ("A" in str(ma_nganh) or ma_nganh.endswith("A")) and award_english:
        bonus += AWARD_ENGLISH_POINTS.get(award_english, 0.0)
    
    return bonus

def parse_to_hop_list(to_hop_data) -> List[List[str]]:
    """Parse dữ liệu tổ hợp thành list of lists"""
    if isinstance(to_hop_data, list):
        if all(isinstance(item, list) for item in to_hop_data):
            # Đã là list of lists
            return to_hop_data
        elif all(isinstance(item, str) for item in to_hop_data):
            # List of strings -> chuyển thành list chứa 1 list
            return [to_hop_data]
    elif isinstance(to_hop_data, str):
        # String -> parse thành list
        subjects = [s.strip() for s in to_hop_data.replace(',', ' ').split()]
        return [subjects] if len(subjects) == 3 else []
    
    return []

def calculate_hocba(hoc_ba, df: pd.DataFrame) -> pd.DataFrame:
    """
    Tính điểm xét tuyển học bạ theo công thức đúng
    
    Args:
        hoc_ba: HocBa object với grade_10, grade_11, grade_12
        df: DataFrame với columns ['ma_nganh', 'to_hop_mon', 'diem_chuan']
            - to_hop_mon có thể là: 
              + List[List[str]]: [["Toán", "Lý", "Hóa"], ["Toán", "Lý", "Anh"]]
              + List[str]: ["Toán", "Lý", "Hóa"] (một tổ hợp duy nhất)
              + str: "Toán,Lý,Hóa" (một tổ hợp duy nhất)
            Optional: ['award_qg', 'award_english']
    
    Returns:
        DataFrame với thêm columns ['best_to_hop_score', 'best_to_hop', 'bonus_points', 'total_score', 'is_passed']
    """
    result_df = df.copy()
    
    # Tính điểm cho từng ngành
    best_scores = []
    best_to_hops = []
    bonus_points = []
    total_scores = []
    is_passed = []
    
    for _, row in result_df.iterrows():
        # Parse tổ hợp môn
        to_hop_list = parse_to_hop_list(row['to_hop_mon'])
        
        # Tính điểm tổ hợp tốt nhất
        best_score, best_to_hop = calculate_best_to_hop_score(hoc_ba, to_hop_list)
        best_scores.append(best_score)
        best_to_hops.append(best_to_hop)
        
        # Tính điểm thưởng
        award_qg = row.get('award_qg')
        award_english = row.get('award_english')
        ma_nganh = row['ma_nganh']
        bonus = calculate_bonus(award_qg, award_english, ma_nganh)
        bonus_points.append(bonus)
        
        # Tổng điểm = Best tổ hợp + Bonus
        total = best_score + bonus
        total_scores.append(total)
        
        # Kiểm tra đậu/rớt
        diem_chuan = row['diem_chuan']
        is_passed.append(total >= diem_chuan)
    
    # Thêm columns mới
    result_df['best_to_hop_score'] = best_scores
    result_df['best_to_hop'] = best_to_hops
    result_df['bonus_points'] = bonus_points
    result_df['total_score'] = total_scores
    result_df['is_passed'] = is_passed
    
    return result_df

def get_subject_scores(hoc_ba, subjects: List[str]) -> Dict[str, float]:
    """Utility function để xem điểm trung bình các môn"""
    return {subject: get_dtbm(hoc_ba, subject) for subject in subjects}

if __name__ == "__main__":
    
    # Test data
    hoc_ba = HocBa(
        grade_10=Grade(toan=7.8, ly=7.5, hoa=7.6, van=7.2, anh=7.9),
        grade_11=Grade(toan=8.2, ly=7.8, hoa=7.9, van=7.4, anh=8.0),
        grade_12=Grade(toan=8.5, ly=8.0, hoa=8.3, van=7.8, anh=8.4)
    )
    
    # Test với ngành có nhiều tổ hợp
    df = pd.DataFrame([
        {
            "ma_nganh": "7480201V",
            "to_hop_mon": [["Toán", "Lý", "Hóa"], ["Toán", "Lý", "Anh"], ["Toán", "Văn", "Anh"]],
            "diem_chuan": 27.45,
            "award_qg": {"level": 2},
            "award_english": None
        },
        {
            "ma_nganh": "7340101 V", 
            "ten_nganh": "Quản trị kinh doanh (Việt)",
            "to_hop_mon": [["Toán", "Văn", "Anh"]],  # Chỉ có 1 tổ hợp
            "diem_chuan": 24.74,
            "award_qg": None,
            "award_english": None
        }
    ])
    
    # Calculate
    result = calculate_hocba(hoc_ba, df)
    
    # Display chi tiết
    print("Điểm trung bình các môn:")
    subjects = ["Toán", "Lý", "Hóa", "Văn", "Anh"]
    subject_scores = get_subject_scores(hoc_ba, subjects)
    for subject, score in subject_scores.items():
        print(f"  {subject}: {score:.2f}")
    
    print("\nKết quả xét tuyển:")
    for _, row in result.iterrows():
        print(f"\n{row['ma_nganh']} - {row['ten_nganh']}")
        print(f"  Tổ hợp tốt nhất: {row['best_to_hop']}")
        print(f"  Điểm tổ hợp: {row['best_to_hop_score']:.2f}")
        print(f"  Điểm thưởng: {row['bonus_points']:.2f}")
        print(f"  Tổng điểm: {row['total_score']:.2f}")
        print(f"  Điểm chuẩn: {row['diem_chuan']:.2f}")
        print(f"  Kết quả: {'ĐẬU' if row['is_passed'] else 'TRƯỢT'}")
    
    # Test manual calculation cho tổ hợp cụ thể
    print(f"\nKiểm tra tính toán thủ công:")
    toan_dtbm = get_dtbm(hoc_ba, "Toán")  # (7.8+8.2+8.5)/3 = 8.17
    ly_dtbm = get_dtbm(hoc_ba, "Lý")      # (7.5+7.8+8.0)/3 = 7.77
    hoa_dtbm = get_dtbm(hoc_ba, "Hóa")    # (7.6+7.9+8.3)/3 = 7.93
    
    to_hop_a00_score = (toan_dtbm * 2 + ly_dtbm + hoa_dtbm) / 4
    print(f"Tổ hợp A00 (Toán, Lý, Hóa): ({toan_dtbm:.2f}*2 + {ly_dtbm:.2f} + {hoa_dtbm:.2f})/4 = {to_hop_a00_score:.2f}")