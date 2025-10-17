from sqlalchemy.orm import Session
from src.core.models import L2UniRequirement

import pandas as pd

def filter_L2_requirements(db: Session, cand_tp, cand_thm, cand_cl, cand_nn)  -> pd.DataFrame:

    query = (
        db.query(L2UniRequirement)
        .filter(L2UniRequirement.province.in_(cand_tp))
        .filter(L2UniRequirement.major_code.in_(cand_nn))
        .filter(L2UniRequirement.subject_combination.in_(cand_thm))
        .filter(L2UniRequirement.uni_type_label.in_(cand_cl))
    )
    return pd.DataFrame(query.all())