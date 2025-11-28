from typing import List
import pandas as pd
from sqlalchemy import Numeric, cast, text
from sqlalchemy.orm import Session

from src.core.models import Admission, TranscriptSujectGroup
from src.services.l3.schemas import UserInputL3


def get_all_transcript_data(db: Session, user_input: UserInputL3) -> pd.DataFrame:
    """
    Lọc dữ liệu L3 từ DB dựa trên UserInputL3, trả về DataFrame.
    """
    query = (
        db.query(Admission)
        .filter(Admission.admission_type.in_(['TỔNG HỢP', 'HỌC BẠ']))
        .filter(Admission.uni_code.in_(['QSB', 'SPK']))
        .filter(Admission.uni_type == user_input.cong_lap_str)
        .filter(Admission.province == user_input.tinh_tp.strip())
        .filter(Admission.major_group == user_input.nhom_nganh)
    )
    if user_input.hoc_phi is not None:
        query = query.filter(cast(Admission.tuition_fee, Numeric) <= user_input.hoc_phi)

    df = pd.read_sql(query.statement, db.bind)
    return df

def get_subject_combination(db: Session, list_major_code: List[str], uni_code: str):
    query = (
        db.query(TranscriptSujectGroup)
        .filter(TranscriptSujectGroup.uni_code == uni_code)
        .filter(TranscriptSujectGroup.major_code.in_(list_major_code))
    )
    df = pd.read_sql(query.statement, db.bind)
    return df