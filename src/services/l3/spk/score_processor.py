import pandas as pd
from typing import Any

from src.services.l3.schema import UserInputL3

from .filters import filter_schools
from src.services.l3.spk.filters import get_to_hop_mon_from_db
from src.services.l3.spk.score_cal import calculate_best_to_hop_score, calculate_bonus, parse_to_hop_from_dataframe

def process_admission_calculation(user_input: UserInputL3, df_schools: pd.DataFrame) -> pd.DataFrame:
    # Bước 1: Lọc trường theo điều kiện
    filtered_schools = filter_schools(df_schools, user_input)
    print(filtered_schools)
    if filtered_schools.empty:
        return pd.DataFrame()
    
    # Bước 2: Lấy tổ hợp môn từ database
    ma_nganh_list = filtered_schools['ma_nganh'].tolist()
    to_hop_data = get_to_hop_mon_from_db(ma_nganh_list)
    print(to_hop_data)
    # Bước 3: Tính điểm học bạ cho từng ngành
    results = []
    
    for _, row in filtered_schools.iterrows():
        ma_nganh = row['ma_nganh']
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
        
        # Thêm vào kết quả
        result_row = row.to_dict()
        result_row.update({
            'to_hop_list': to_hop_list,
            'best_to_hop': best_to_hop,
            'best_to_hop_score': round(best_score, 2),
            'bonus_points': round(bonus, 2),
            'total_score': round(total_score, 2)
        })
        results.append(result_row)
    
    if not results:
        return pd.DataFrame()
    
    result_df = pd.DataFrame(results)
    # Sắp xếp theo điểm từ cao xuống thấp
    result_df = result_df.sort_values('total_score', ascending=False)
    
    return result_df

if __name__ == "__main__":
    
    df_schools = pd.read_excel("data/hocba_l3.xlsx")
    
    from src.services.l3.schema import HocBa, Grade, AwardQG, AwardEnglish, UserInputL3
    
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
    print(result_df.head(10))