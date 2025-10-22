import pandas as pd
from typing import List
from sqlalchemy.orm import Session

from src.core.models import Admission
from src.services.l1.schema import L1PredictResult

def get_major_code_satisfied_tuition_fee(db: Session, results: List[str], user_budget: int) -> List[L1PredictResult]:
    query = db.query(Admission).filter(Admission.admission_code.in_(results)).filter(Admission.tuition_fee <= user_budget)
    return pd.read_sql(query.statement, db.bind)