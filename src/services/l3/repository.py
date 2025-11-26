from typing import List
import pandas as pd
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.core.models import L3Transcript, TranscriptSujectGroup
from src.services.l3.schemas import UserInputL3


def get_all_transcript_data(db: Session, user_input: UserInputL3) -> pd.DataFrame:
    """
    Lọc dữ liệu L3 từ DB dựa trên UserInputL3, trả về DataFrame.
    """
    query = (
        db.query(L3Transcript)
        .filter(L3Transcript.uni_type == user_input.cong_lap)
        .filter(L3Transcript.province == user_input.tinh_tp.strip())
        .filter(L3Transcript.major_group == user_input.nhom_nganh.value)
    )

    if user_input.hoc_phi is not None:
        query = query.filter(L3Transcript.tuition_fee <= user_input.hoc_phi)

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