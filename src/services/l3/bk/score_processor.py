from typing import List
import pandas as pd

from src.services.l3.bk.score_cal2 import calculate_type1, calculate_type2, parse_to_hop_from_dataframe
from src.services.l3.schemas import UserInputL3
from src.services.l3.bk.filter import filter_schools, get_to_hop_mon_from_db

# Import the BK schemas with aliases to avoid confusion
from src.services.l3.bk.schema import (
    AdmissionInputType1, 
    AdmissionInputType2, 
    CEFRLevel
)

from src.services.l3.schemas import (
    TNTHPTScores as BK_TNTHPTScores,
    SubjectScores as BK_SubjectScores,
    HocBa as BK_HighSchoolTranscript,
    Grade as BK_Grade,
    DGNL as BK_DGNL,
)
from src.services.l3.repository import get_subject_combination

def convert_hoc_ba_to_high_school_transcript(hoc_ba):
    """Convert HocBa to HighSchoolTranscript"""
    def convert_grade(grade):
        return BK_Grade(
            toan=grade.toan,
            ly=grade.ly,
            hoa=grade.hoa,
            van=grade.van,
            anh=grade.anh,
            sinh=grade.sinh,
            su=grade.su,
            dia=grade.dia,
            tin=grade.tin,
            gdkt_pl=grade.gdkt_pl,
            cong_nghe=getattr(grade, 'cong_nghe_cong_nghiep', None)
        )
    
    return BK_HighSchoolTranscript(
        grade_10=convert_grade(hoc_ba.grade_10),
        grade_11=convert_grade(hoc_ba.grade_11),
        grade_12=convert_grade(hoc_ba.grade_12)
    )

def convert_thpt_scores(thpt_scores):
    """Convert TNTHPTScores from schemas.py to BK TNTHPTScores"""
    return BK_TNTHPTScores(
        math_score=BK_SubjectScores(
            subject_name=thpt_scores.math_score.subject_name,
            score=thpt_scores.math_score.score
        ),
        literature_score=BK_SubjectScores(
            subject_name=thpt_scores.literature_score.subject_name,
            score=thpt_scores.literature_score.score
        ),
        elective_1_score=BK_SubjectScores(
            subject_name=thpt_scores.elective_1_score.subject_name,
            score=thpt_scores.elective_1_score.score
        ),
        elective_2_score=BK_SubjectScores(
            subject_name=thpt_scores.elective_2_score.subject_name,
            score=thpt_scores.elective_2_score.score
        )
    )

def convert_dgnl_scores(dgnl):
    """Convert DGNL from schemas.py to BK DGNL"""
    return BK_DGNL(
        language_score=dgnl.language_score,
        math_score=dgnl.math_score,
        science_logic=dgnl.science_logic
    )

def convert_english_cert(award_english):
    """Convert english certificate level to CEFRLevel"""
    if not award_english:
        return None
    
    level_mapping = {
        "B1": CEFRLevel.B1,
        "B2": CEFRLevel.B2,
        "C1": CEFRLevel.C1,
        "C2": CEFRLevel.C2
    }
    
    return level_mapping.get(award_english.level)

def convert_input_to_type1(user_input: UserInputL3):
    """Convert UserInputL3 to AdmissionInputType1 with proper type conversion"""
    # Convert TNTHPTScores - handle both dict and object formats
    if isinstance(user_input.thpt, dict):
        # If it's already a dict, convert to the UserInputL3 TNTHPTScores first
        from src.services.l3.schemas import TNTHPTScores, SubjectScores
        thpt_obj = TNTHPTScores(**user_input.thpt)
    else:
        thpt_obj = user_input.thpt
    
    return AdmissionInputType1(
        dgnl_score=convert_dgnl_scores(user_input.dgnl),
        tnthpt_scores=convert_thpt_scores(thpt_obj),
        high_school_grades=convert_hoc_ba_to_high_school_transcript(user_input.hoc_ba),
        subject_combination=getattr(user_input, 'subject_combination', []),
        priority_region=user_input.priority_region,
        priority_object=user_input.priority_object,
        english_cert=convert_english_cert(user_input.award_english)
    )

def convert_input_to_type2(user_input: UserInputL3):
    """Convert UserInputL3 to AdmissionInputType2 with proper type conversion"""
    # Convert TNTHPTScores - handle both dict and object formats
    if isinstance(user_input.thpt, dict):
        # If it's already a dict, convert to the UserInputL3 TNTHPTScores first
        from src.services.l3.schemas import TNTHPTScores, SubjectScores
        thpt_obj = TNTHPTScores(**user_input.thpt)
    else:
        thpt_obj = user_input.thpt
    
    return AdmissionInputType2(
        tnthpt_scores=convert_thpt_scores(thpt_obj),
        high_school_grades=convert_hoc_ba_to_high_school_transcript(user_input.hoc_ba),
        subject_combination=getattr(user_input, 'subject_combination', []),
        priority_region=user_input.priority_region,
        priority_object=user_input.priority_object,
        english_cert=convert_english_cert(user_input.award_english)
    )

def validate_user_input(user_input: UserInputL3) -> bool:
    """
    Validate user input data.
    
    Args:
        user_input: User input to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    # Check if at least one score type is provided
    has_scores = any([
        user_input.dgnl,
        user_input.thpt,
        user_input.hoc_ba
    ])
    
    if not has_scores:
        print("No scores provided in user input")
        return False
        
    return True

def process_admission_calculation(db, user_input: UserInputL3, df_schools: pd.DataFrame, uni_code: str) -> pd.DataFrame:
    # Lấy tổ hợp môn từ database
    ma_nganh_list = df_schools['major_code'].tolist()
    
    to_hop_data = get_subject_combination(db, ma_nganh_list, uni_code)
    to_hop_list = to_hop_data["subject_combination"].to_list()
    
    # Bước 3: Nếu trong user input có đánh giá năng lực thì tính công thức 1, nếu không có tính công thức 2
    results = []

    for _, row in df_schools.iterrows():
        ma_nganh = row['major_code']
        print(f"Ngành: {ma_nganh}")
        ten_nganh = row.get('major_name', '')
        diem_chuan = row.get('score', 0.0)  
        nhom_nganh = int(row.get('major_group', user_input.nhom_nganh))

        to_hop_list = parse_to_hop_from_dataframe(to_hop_data, ma_nganh)
        print(f"Tổ hợp: {to_hop_list}")
        
        if not to_hop_list:
            continue
        
        # Tính điểm cho tất cả các tổ hợp và chọn tổ hợp tốt nhất
        best_score = -1
        best_combination = []
        
        for to_hop in to_hop_list:
            # Create updated user input with current subject combination
            user_input_updated = user_input.model_copy(update={"subject_combination": [to_hop]})
            print(f"Calculating for combination: {to_hop}")
            if user_input_updated.dgnl:
                current_score = calculate_type1(convert_input_to_type1(user_input_updated), to_hop)
            else:
                current_score = calculate_type2(convert_input_to_type2(user_input_updated), to_hop)

            if current_score > best_score:
                best_score = current_score
                best_combination = to_hop

        # Calculate bonus points (priority points)
        bonus_points = float(user_input.priority_region) + float(user_input.priority_object)
        
        # Total score = best_score + bonus_points (best_score already includes priority calculation)
        # So I just use best_score as total_score since priority is already included in the calculation
        total_score = best_score
        
        # Create result record
        result = {
            'ma_nganh': ma_nganh,
            'ten_nganh': ten_nganh,
            'diem_chuan': round(diem_chuan, 2),
            'nhom_nganh': nhom_nganh,
            'best_to_hop': best_combination,
            'best_to_hop_score': round(best_score, 2),
            'bonus_points': round(bonus_points, 2),
            'total_score': round(total_score, 2)
        }
        
        results.append(result)
    # Bước 4: Trả về kết quả
    df_results = pd.DataFrame(results)
    
    # Bước 5: Filter: chỉ giữ những ngành có total_score >= diem_chuan
    df_filtered = df_results[df_results['total_score'] >= df_results['diem_chuan']]
    
    # Bước 6: Sort by total_score descending để xem ngành nào có khả năng đỗ cao nhất
    df_filtered = df_filtered.sort_values('total_score', ascending=False)
    
    return df_filtered.reset_index(drop=True)

if __name__ == "__main__":
    df_schools = pd.read_excel("data/bk_hb_l3.xlsx")
    from src.services.l3.schemas import UserInputL3, HocBa, Grade, AwardQG, AwardEnglish, TNTHPTScores, SubjectScores
    
    hoc_ba = HocBa(
        grade_10=Grade(toan=9.0, ly=8.5, hoa=8.0, van=7.5, anh=9.0),
        grade_11=Grade(toan=9.5, ly=9.0, hoa=8.5, van=8.0, anh=9.5),
        grade_12=Grade(toan=10.0, ly=9.5, hoa=9.0, van=8.5, anh=10.0)
    )

    award_qg = AwardQG(subject="Toán", level=2)
    award_english = AwardEnglish(level="C1")

    thpt = TNTHPTScores(
        math_score=SubjectScores(subject_name="Toán", score=8.5),
        elective_1_score=SubjectScores(subject_name="Anh", score=8.0),
        elective_2_score=SubjectScores(subject_name="Lý", score=7.5),
        literature_score=SubjectScores(subject_name="Văn", score=7.0)
    )
    
    dgnl = BK_DGNL(
        language_score=295,
        math_score=270,
        science_logic=400
    )

    user_input = UserInputL3(
        cong_lap=1,
        tinh_tp="TP. Hồ Chí Minh",
        hoc_phi=50000000,
        nhom_nganh=752,
        hoc_ba=hoc_ba,
        award_qg=award_qg,
        award_english=award_english,
        thpt=thpt,
        dgnl=dgnl.model_dump()
    )
    
    result_df = process_admission_calculation(user_input, df_schools)
    print("RESULT: \n", result_df.head(10))