from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import json, lightgbm as lgb
import pandas as pd
from pandas.api.types import CategoricalDtype
import re
from typing import List, Iterable

from src.services.l2.schema import UserInputL2, L2PredictResult
from src.services.l2.preprocess import input_to_pairs_L2
from src.core.config import logger

@dataclass
class L2Predictor:
    booster: lgb.Booster
    feature_names: list[str]
    cat_vocab: dict[str, list[str]]
    threshold: float

    @classmethod
    def load(cls, model_dir: Path, threshold: float) -> "L2Predictor":
        logger.info(f"Loading L2 predictor from {model_dir}")
        mroot = Path(model_dir, "user_item_lightgbm")
        booster = lgb.Booster(model_file=str(mroot / "l2_lightgbm.txt"))
        feature_names = json.loads((mroot / "feature_names.json").read_text(encoding="utf-8"))
        cat_vocab = json.loads((mroot / "cat_vocab.json").read_text(encoding="utf-8"))

        logger.debug(f"Loaded booster with {len(feature_names)} features and {len(cat_vocab)} categorical columns")

        # Clean vocab
        for c, vocab in cat_vocab.items():
            vs = []
            seen = set()
            for v in (str(x) for x in vocab if x is not None):
                if v not in seen:
                    seen.add(v)
                    vs.append(v)
            if "__UNK__" in vs:
                vs.remove("__UNK__")
            cat_vocab[c] = ["__UNK__"] + vs
        logger.info("Categorical vocab cleaned")
        return cls(booster=booster, feature_names=feature_names, cat_vocab=cat_vocab, threshold=threshold)

    def _prep_df_for_predict(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.debug(f"Preparing DataFrame for prediction, shape={df.shape}")
        df = df.copy()
        for c, vocab in self.cat_vocab.items():
            if c in df.columns:
                s = df[c].astype(str)
                s.loc[~s.isin(vocab)] = "__UNK__"
                df[c] = s.astype(CategoricalDtype(categories=vocab, ordered=False))
        for f in self.feature_names:
            if f not in df.columns:
                df[f] = pd.NA
        cat_keys = set(self.cat_vocab.keys())
        for f in self.feature_names:
            if f not in cat_keys:
                df[f] = pd.to_numeric(df[f], errors="coerce")
        df = df.reindex(columns=self.feature_names)
        logger.debug(f"Prepared DataFrame columns: {df.columns.tolist()}")
        return df

    def predict(self, user: UserInputL2) -> list[L2PredictResult]:
        logger.info("Starting L2 prediction")
        processed = input_to_pairs_L2(user)
        if isinstance(processed, pd.DataFrame) and processed.empty:
            logger.warning("No processed data after input_to_pairs_L2")
            return []

        X = self._prep_df_for_predict(processed)
        if X.shape[0] == 0:
            logger.warning("No data to predict after preprocessing")
            return []

        niter = self.booster.best_iteration or self.booster.current_iteration() or -1
        score = self.booster.predict(X, num_iteration=niter)
        logger.debug(f"Predicted scores: {score}")

        out = processed.copy()
        out["score"] = score

        top = (
            out.loc[out["score"] >= self.threshold, ["cand_ma_xet_tuyen", "score"]]
            .assign(cand_ma_xet_tuyen=lambda df: df["cand_ma_xet_tuyen"].astype(str))
            .sort_values("score", ascending=False)
            .drop_duplicates(subset="cand_ma_xet_tuyen", keep="first")
            .reset_index(drop=True)
        )

        result = [L2PredictResult(ma_xet_tuyen=r["cand_ma_xet_tuyen"], score=r["score"]) for _, r in top.iterrows()]
        logger.info(f"{len(result)} candidates passed threshold {self.threshold}")
        return discount_fee(user, result)

_CEFR_RE = re.compile(r"\b(A1|A2|B1|B2|C1|C2)\b", re.I)

def _has_cefr(val: str | None, targets: Iterable[str]) -> bool:
    if not val:
        return False
    s = str(val).upper()
    m = _CEFR_RE.search(s)
    if m:
        return m.group(1) in {t.upper() for t in targets}
    return any(t.upper() in s for t in targets)

def discount_fee(input: UserInputL2, results: List["L2PredictResult"]) -> List["L2PredictResult"]:
    try:
        score = float(input.diem_chuan)
    except Exception:
        score = 0.0
        logger.warning(f"Invalid diem_chuan: {input.diem_chuan}")

    try:
        budget = float(input.hoc_phi)
    except Exception:
        budget = 0.0
        logger.warning(f"Invalid hoc_phi: {input.hoc_phi}")

    out: List["L2PredictResult"] = []
    for r in results:
        code = str(r.ma_xet_tuyen)
        if code.startswith("UEF") and code.endswith("THPTQG"):
            tier1 = ((21 <= score < 24) or _has_cefr(input.diem_ccta, {"A2"})) and (budget >= 60_000_000)
            tier2 = ((24 <= score < 27) or _has_cefr(input.diem_ccta, {"B1", "B2"})) and (budget >= 40_000_000)
            tier3 = ((27 <= score <= 30) or _has_cefr(input.diem_ccta, {"C1", "C2"})) and (budget >= 0)
            if tier1 or tier2 or tier3:
                out.append(r)
        else:
            out.append(r)
    logger.debug(f"After discount_fee: {len(out)} candidates remain from {len(results)}")
    return out
