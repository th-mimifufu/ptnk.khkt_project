import pandas as pd

from src.services.l3.repository import get_subject_combination
from src.services.l3.schemas import UserInputL3
from src.services.l3.schemas import HocBa, Grade, AwardQG, AwardEnglish, UserInputL3

from src.services.l3.spk.score_cal import calculate_best_to_hop_score, calculate_bonus, parse_to_hop_from_dataframe
from src.core.config import logger

def process_admission_calculation(db, user_input: UserInputL3, df_schools: pd.DataFrame, uni_code: str) -> pd.DataFrame:
    """Tính điểm và lọc ngành dựa trên học bạ + giải thưởng."""
    logger.info("Start process_admission_calculation")
    
    # Lấy tổ hợp môn từ database
    ma_nganh_list = df_schools['major_code'].tolist()
    logger.debug(f"Major codes: {ma_nganh_list}")

    to_hop_data = get_subject_combination(db, ma_nganh_list, uni_code)
    logger.debug(f"Retrieved subject combination data: {len(to_hop_data)} rows")
    
    results = []

    for _, row in df_schools.iterrows():
        ma_nganh = row['major_code']
        ten_nganh = row['major_name']
        diem_chuan = row['score']
        nhom_nganh = int(row.get('major_group', user_input.nhom_nganh))
        admission_code = row['admission_code']
        uni_name = row['uni_name']
        uni_type = row['uni_type']
        
        if uni_type == 1:
            uni_type = "Công lập"
        else:
            uni_type = "Tư thục"

        province = row['province']
        uni_web_name = row['uni_web_link']
        study_program = row['study_program']
        admission_type = row['admission_type']
        admission_type_name = row['admission_type_name']
        tuition_fee = row['tuition_fee']


        logger.debug(f"Processing major {ma_nganh} - {ten_nganh}")

        to_hop_list = parse_to_hop_from_dataframe(to_hop_data, ma_nganh)
        logger.debug(f"Parsed {len(to_hop_list)} subject combinations: {to_hop_list}")
        if not to_hop_list:
            continue

        best_score, best_to_hop = calculate_best_to_hop_score(user_input.hoc_ba, to_hop_list)
        logger.debug(f"Best combination for {ma_nganh}: {best_to_hop} -> {best_score}")

        bonus = calculate_bonus(user_input.award_qg, user_input.award_english, ma_nganh)
        logger.debug(f"Bonus points for {ma_nganh}: {bonus}")

        total_score = best_score + bonus
        logger.info(f"Major {ma_nganh} -> Total score: {total_score}")

        result = {
            'admission_code': admission_code,
            'uni_code': uni_code,
            'uni_name': uni_name,
            'uni_type': uni_type,
            'province': province,
            'uni_web_name': uni_web_name,
            'study_program': study_program,
            'admission_type': admission_type,
            'admission_type_name': admission_type_name,
            'major_code': ma_nganh,
            'major_name': ten_nganh,
            'uni_score': round(diem_chuan, 2),
            'major_group': nhom_nganh,
            'tuition_fee': tuition_fee,
            'subject_combination': best_to_hop,
            'best_subject_combination_score': round(best_score, 2),
            'bonus_points': round(bonus, 2),
            'best_subject_combination_total_score': round(total_score, 2)
        }

        results.append(result)

    if not results:
        logger.warning("No results calculated")
        return pd.DataFrame()

    result_df = pd.DataFrame(results)
    df_filtered = result_df[result_df['best_subject_combination_total_score'] >= result_df['uni_score']]
    df_filtered = df_filtered.sort_values('best_subject_combination_total_score', ascending=False)

    logger.info(f"Processed {len(df_filtered)} majors after filtering")
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

    result_df = process_admission_calculation(None, user_input, df_schools, uni_code="BK001")
    logger.info("Finished processing")
    # print(result_df.head(10))
