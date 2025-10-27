import pandas as pd

from src.services.l3.repository import get_subject_combination
from src.services.l3.schemas import UserInputL3
from src.services.l3.schemas import HocBa, Grade, AwardQG, AwardEnglish, UserInputL3

from src.services.l3.spk.score_cal import calculate_best_to_hop_score, calculate_bonus, parse_to_hop_from_dataframe

def process_admission_calculation(db, user_input: UserInputL3, df_schools: pd.DataFrame, uni_code: str) -> pd.DataFrame:
    # Lấy tổ hợp môn từ database
    ma_nganh_list = df_schools['major_code'].tolist()
    
    to_hop_data = get_subject_combination(db, ma_nganh_list, uni_code)
    to_hop_list = to_hop_data["subject_combination"].to_list()

    # Tính điểm học bạ cho từng ngành
    results = []
    
    for _, row in df_schools.iterrows():
        ma_nganh = row['major_code']
        ten_nganh = row.get('major_name', '')
        diem_chuan = row.get('score', 0.0)  
        nhom_nganh = int(row.get('major_group', user_input.nhom_nganh))

        print(f"Ngành: {ma_nganh}")
        to_hop_list = parse_to_hop_from_dataframe(to_hop_data, ma_nganh)
        print(f"Tổ hợp: {to_hop_list}")
        if not to_hop_list:
            continue
        
        # Tính điểm tổ hợp tốt nhất
        best_score, best_to_hop = calculate_best_to_hop_score(user_input.hoc_ba, to_hop_list)
        print(f"Ngành {ma_nganh}, Tổ hợp {best_to_hop}, Điểm {best_score}")
        # Tính điểm thưởng
        bonus = calculate_bonus(user_input.award_qg, user_input.award_english, ma_nganh)
        
        # Tổng điểm
        total_score = best_score + bonus
        
        # Create result record
        result = {
            'ma_nganh': ma_nganh,
            'ten_nganh': ten_nganh,
            'diem_chuan': round(diem_chuan, 2),
            'nhom_nganh': nhom_nganh,
            'best_to_hop': best_to_hop,
            'best_to_hop_score': round(best_score, 2),
            'bonus_points': round(bonus, 2),
            'total_score': round(total_score, 2)
        }

        # # Thêm vào kết quả
        # result_row = row.to_dict()
        # result_row.update({
        #     'to_hop_list': to_hop_list,
        #     'best_to_hop': best_to_hop,
        #     'best_to_hop_score': round(best_score, 2),
        #     'bonus_points': round(bonus, 2),
        #     'total_score': round(total_score, 2)
        # })
        results.append(result)
    
    if not results:
        return pd.DataFrame()
    
    result_df = pd.DataFrame(results)

    df_filtered = result_df[result_df['total_score'] >= result_df['diem_chuan']]
    # Sắp xếp theo điểm từ cao xuống thấp
    df_filtered = df_filtered.sort_values('total_score', ascending=False)
    return df_filtered

if __name__ == "__main__":
    
    df_schools = pd.read_excel("data/hocba_l3.xlsx")
    
    hoc_ba = HocBa(
        grade_10=Grade(toan=9.0, ly=8.5, hoa=8.0, van=7.5, anh=9.0),
        grade_11=Grade(toan=9.5, ly=9.0, hoa=8.5, van=8.0, anh=9.5),
        grade_12=Grade(toan=10.0, ly=9.5, hoa=9.0, van=8.5, anh=10.0)
    )

    award_qg = AwardQG(subject="Toán", level=2)
    award_english = AwardEnglish(level="B2")
    
    user_input = UserInputL3(
        cong_lap=1,
        tinh_tp="TP. Hồ Chí Minh",
        hoc_phi=50000000,
        nhom_nganh=781,
        hoc_ba=hoc_ba,
        award_qg=award_qg,
        award_english=award_english
    )
    
    result_df = process_admission_calculation(user_input, df_schools)
    print("RESULT: \n", result_df.head(10))