from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import joblib
import json
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Tuple

from src.core.config import logger
from src.core.database import SessionLocal
from src.services.l1.repository import get_major_code_satisfied_tuition_fee
from src.services.l1.schema import UserInputL1, L1PredictResult
from src.services.l1.preprocess import preprocess_input_data_L1

@dataclass
class L1Predictor:
    models: Dict[Tuple, Any]
    encoders: Dict[Tuple, Any]
    label_encoders: Dict[Tuple, Any]
    class_lists: Dict[Tuple, List[str]]
    group_cols: List[str]
    ohe_cols: List[str]

    @classmethod
    def load(cls, model_dir: Path) -> "L1Predictor":
        logger.info(f"Loading L1 predictor from {model_dir}")
        root = Path(model_dir)
        # Load artifacts
        try:
            models = joblib.load(root / "models.pkl")
            encoders = joblib.load(root / "encoders.pkl")
            label_encoders = joblib.load(root / "label_encoders.pkl")
            class_lists = joblib.load(root / "class_lists.pkl")
            logger.info("Loaded model artifacts successfully (pkl files)")
        except Exception:
            bundle = joblib.load(root / "l1_model_group_wise.joblib")
            models = bundle["models"]
            encoders = bundle["encoders"]
            label_encoders = bundle["label_encoders"]
            class_lists = bundle["class_lists"]
            logger.warning("Loaded model artifacts from legacy joblib bundle")

        try:
            group_cols = json.loads((root / "group_cols.json").read_text(encoding="utf-8"))
        except Exception:
            group_cols = ["tinh_tp", "nhom_nganh"]
            logger.warning("Failed to load group_cols.json, using default")

        try:
            ohe_cols = json.loads((root / "ohe_cols.json").read_text(encoding="utf-8"))
        except Exception:
            ohe_cols = ["cong_lap","tinh_tp","nhom_nganh","hsg_subject","ahld","dan_toc_thieu_so","haimuoi_huyen_ngheo_tnb"]
            logger.warning("Failed to load ohe_cols.json, using default")

        logger.info("L1 predictor loaded successfully")
        return cls(models=models, encoders=encoders, label_encoders=label_encoders, class_lists=class_lists, group_cols=group_cols, ohe_cols=ohe_cols)
    
    @staticmethod
    def infer_loai_uu_tien(row: pd.Series) -> str:
        subj = str(row.get('hsg_subject', '0'))
        if subj not in ('0', 'UNK', 'None', 'nan', ''):
            return f"HSG {subj}"
        if int(row.get('ahld', 0)) == 1:
            return "AHLD"
        if int(row.get('dan_toc_thieu_so', 0)) == 1:
            return "Dân tộc thiểu số"
        if int(row.get('haimuoi_huyen_ngheo_tnb', 0)) == 1:
            return "50 huyện nghèo/TNB"
        return "Không ưu tiên"

    def predict(self, user: UserInputL1) -> List[L1PredictResult]:
        logger.info(f"Start predicting L1 for user with hoc_phi={user.hoc_phi}")
        processed_data = preprocess_input_data_L1(user).reset_index(drop=True)
        logger.debug(f"Processed data: \n{processed_data.head()}")

        if processed_data.empty:
            logger.info("No valid rows after preprocessing, returning default result")
            return [L1PredictResult(loai_uu_tien="Không ưu tiên", ma_xet_tuyen={})]

        processed_data = processed_data.assign(row_id=lambda d: d.index)
        results: List[L1PredictResult] = []

        for _, r in processed_data.iterrows():
            gkey = tuple(r[c] for c in self.group_cols)
            loai = self.infer_loai_uu_tien(r)
            logger.debug(f"Row {r['row_id']}: group_key={gkey}, loai_uu_tien={loai}")

            if loai == "Không ưu tiên" or gkey not in self.models:
                results.append(L1PredictResult(loai_uu_tien=loai, ma_xet_tuyen={}))
                logger.debug(f"Skipping prediction for row {r['row_id']}")
                continue

            clf = self.models[gkey]
            enc = self.encoders.get(gkey)
            le = self.label_encoders.get(gkey)
            cls_list = self.class_lists.get(gkey, [])

            if clf is None:
                out_map = {cls_list[0]: 1.0} if cls_list else {}
                results.append(L1PredictResult(loai_uu_tien=loai, ma_xet_tuyen=out_map))
                logger.debug(f"No classifier for group {gkey}, using default class list")
                continue

            feat_in = (
                list(enc.feature_names_in_)
                if hasattr(enc, "feature_names_in_") and enc.feature_names_in_ is not None
                else self.ohe_cols
            )

            x_df = r[feat_in].astype(str).to_frame().T
            X = enc.transform(x_df) if enc is not None else x_df

            out_map = {}
            if hasattr(clf, "predict_proba"):
                p = clf.predict_proba(X)[0]
                s = float(p.sum())
                if s <= 0:
                    logger.warning(f"Sum of predicted probabilities <= 0 for row {r['row_id']}")
                    results.append(L1PredictResult(loai_uu_tien=loai, ma_xet_tuyen={}))
                    continue
                order = np.argsort(p)[::-1]
                labels_sorted = (
                    le.classes_[order] if le is not None else np.array(cls_list)[order]
                )
                probs_sorted = (p[order] / s).astype(float)
                out_map = {str(lab): float(pr) for lab, pr in zip(labels_sorted, probs_sorted)}
            else:
                yhat = clf.predict(X)[0]
                pred = (
                    le.inverse_transform([yhat])[0]
                    if le is not None
                    else (cls_list[int(yhat)] if cls_list else None)
                )
                out_map = {str(pred): 1.0} if pred is not None else {}

            # Lọc học phí
            db = SessionLocal()
            try:
                if out_map:
                    valid_codes = list(out_map.keys())
                    df_valid = get_major_code_satisfied_tuition_fee(db, valid_codes, user.hoc_phi)
                    allowed_codes = set(df_valid["admission_code"].tolist())
                    out_map = {k: v for k, v in out_map.items() if k in allowed_codes}
                    logger.debug(f"Row {r['row_id']}: filtered admission codes by hoc_phi, remaining={list(out_map.keys())}")
            finally:
                db.close()

            results.append(L1PredictResult(loai_uu_tien=loai, ma_xet_tuyen=out_map))

        logger.info("Finished L1 prediction")
        return results
