from typing import List
import pandas as pd
from src.core.config import logger

from src.services.l3.bk.score_cal2 import calculate_type1, calculate_type2, parse_to_hop_from_dataframe
from src.services.l3.schemas import UserInputL3
from src.services.l3.bk.filter import filter_schools, get_to_hop_mon_from_db

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
    logger.debug("Converting HocBa → HighSchoolTranscript…")

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
            cong_nghe=grade.cong_nghe
        )

    return BK_HighSchoolTranscript(
        grade_10=convert_grade(hoc_ba.grade_10),
        grade_11=convert_grade(hoc_ba.grade_11),
        grade_12=convert_grade(hoc_ba.grade_12)
    )


def convert_thpt_scores(thpt_scores):
    logger.debug("Converting TNTHPT scores…")
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
        ),
    )


def convert_dgnl_scores(dgnl):
    logger.debug("Converting DGNL scores…")
    return BK_DGNL(
        language_score=dgnl.language_score,
        math_score=dgnl.math_score,
        science_logic=dgnl.science_logic
    )


def convert_english_cert(award_english):
    if not award_english:
        return None

    logger.debug(f"Converting English certificate: {award_english.level}")

    level_mapping = {
        "B1": CEFRLevel.B1,
        "B2": CEFRLevel.B2,
        "C1": CEFRLevel.C1,
        "C2": CEFRLevel.C2,
    }
    return level_mapping.get(award_english.level)


def convert_input_to_type1(user_input: UserInputL3):
    logger.info("Converting input → Type1 Admission model…")

    if isinstance(user_input.thpt, dict):
        from src.services.l3.schemas import TNTHPTScores
        thpt_obj = TNTHPTScores(**user_input.thpt)
    else:
        thpt_obj = user_input.thpt

    return AdmissionInputType1(
        dgnl_score=convert_dgnl_scores(user_input.dgnl),
        tnthpt_scores=convert_thpt_scores(thpt_obj),
        high_school_grades=convert_hoc_ba_to_high_school_transcript(user_input.hoc_ba),
        subject_combination=getattr(user_input, "subject_combination", []),
        priority_region=user_input.priority_region,
        priority_object=user_input.priority_object,
        english_cert=convert_english_cert(user_input.award_english),
    )


def convert_input_to_type2(user_input: UserInputL3):
    logger.info("Converting input → Type2 Admission model…")

    if isinstance(user_input.thpt, dict):
        from src.services.l3.schemas import TNTHPTScores
        thpt_obj = TNTHPTScores(**user_input.thpt)
    else:
        thpt_obj = user_input.thpt

    return AdmissionInputType2(
        tnthpt_scores=convert_thpt_scores(thpt_obj),
        high_school_grades=convert_hoc_ba_to_high_school_transcript(user_input.hoc_ba),
        subject_combination=getattr(user_input, "subject_combination", []),
        priority_region=user_input.priority_region,
        priority_object=user_input.priority_object,
        english_cert=convert_english_cert(user_input.award_english),
    )


def validate_user_input(user_input: UserInputL3) -> bool:
    logger.info("Validating user input…")

    has_scores = any([user_input.dgnl, user_input.thpt, user_input.hoc_ba])

    if not has_scores:
        logger.warning("User input invalid: no scores provided")
        return False

    return True


def process_admission_calculation(db, user_input: UserInputL3, df_schools: pd.DataFrame, uni_code: str) -> pd.DataFrame:
    logger.info("Starting admission calculation…")

    ma_nganh_list = df_schools["major_code"].tolist()
    to_hop_data = get_subject_combination(db, ma_nganh_list, uni_code)

    results = []

    for _, row in df_schools.iterrows():
        ma_nganh = row['major_code']
        logger.debug(f"Processing major: {ma_nganh}")

        id = row['id']
        ten_nganh = row['major_name']
        diem_chuan = row['score']
        nhom_nganh = int(row.get('major_group', user_input.nhom_nganh))
        admission_code = row['admission_code']
        uni_name = row['uni_name']
        uni_type = row['uni_type']
        province = row['province']
        uni_web_link = row['uni_web_link']
        study_program = row['study_program']
        admission_type = row['admission_type']
        admission_type_name = row['admission_type_name']
        tuition_fee = row['tuition_fee']

        to_hop_list = parse_to_hop_from_dataframe(to_hop_data, ma_nganh)
        if not to_hop_list:
            logger.debug(f"No subject combinations for {ma_nganh}")
            continue

        best_score = -1
        best_combination = []

        for to_hop in to_hop_list:
            user_input_updated = user_input.model_copy(update={"subject_combination": [to_hop]})

            if user_input_updated.dgnl:
                current_score = calculate_type1(convert_input_to_type1(user_input_updated), to_hop)
            else:
                current_score = calculate_type2(convert_input_to_type2(user_input_updated), to_hop)

            if current_score > best_score:
                best_score = current_score
                best_combination = to_hop

        bonus_points = float(user_input.priority_region) + float(user_input.priority_object)
        total_score = best_score

        results.append(
            {
            'id': id, 
            'admission_code': admission_code,
            'uni_code': uni_code,
            'uni_name': uni_name,
            'uni_type': uni_type,
            'province': province,
            'uni_web_link': uni_web_link,
            'study_program': study_program,
            'admission_type': admission_type,
            'admission_type_name': admission_type_name,
            'major_code': ma_nganh,
            'major_name': ten_nganh,
            'uni_score': round(diem_chuan, 2),
            'major_group': nhom_nganh,
            'tuition_fee': tuition_fee,
            'subject_combination': best_combination,
            'best_subject_combination_score': round(best_score, 2),
            'bonus_points': round(bonus_points, 2),
            'best_subject_combination_total_score': round(total_score, 2)
        }
        )

    df_results = pd.DataFrame(results)
    df_filtered = df_results[df_results["best_subject_combination_total_score"] >= df_results["uni_score"]]
    df_filtered = df_filtered.sort_values("best_subject_combination_total_score", ascending=False)

    logger.info("Admission calculation completed.")

    return df_filtered.reset_index(drop=True)
