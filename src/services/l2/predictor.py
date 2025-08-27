from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import json, lightgbm as lgb
import pandas as pd
from pandas.api.types import CategoricalDtype
import re
from typing import List, Iterable

from src.services.l2.schema import UserInputL2, L2PredictResult
from src.services.l2.preprocess import preprocess_input_data_L2

@dataclass
class L2Predictor:
    booster: lgb.Booster
    feature_names: list[str]
    cat_vocab: dict[str, list[str]]
    threshold: float

    @classmethod
    def load(cls, model_dir: Path, threshold: float) -> "L2Predictor":
        mroot = Path(model_dir, "user_item_lightgbm")
        booster = lgb.Booster(model_file=str(mroot / "l2_lightgbm.txt"))
        feature_names = json.loads((mroot / "feature_names.json").read_text(encoding="utf-8"))
        cat_vocab = json.loads((mroot / "cat_vocab.json").read_text(encoding="utf-8"))

        # Clean vocab
        for c, vocab in cat_vocab.items():
            vs = []
            seen = set()
            for v in (str(x) for x in vocab if x is not None):
                if v not in seen:
                    seen.add(v); vs.append(v)
            if "__UNK__" in vs: vs.remove("__UNK__")
            cat_vocab[c] = ["__UNK__"] + vs
        return cls(booster=booster, feature_names=feature_names, cat_vocab=cat_vocab, threshold=threshold)

    def _prep_df_for_predict(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        for c, vocab in self.cat_vocab.items():
            if c in df.columns:
                s = df[c].astype(str)
                s.loc[~s.isin(vocab)] = "__UNK__"
                df[c] = s.astype(CategoricalDtype(categories=vocab, ordered=False))
        for f in self.feature_names:
            if f not in df.columns: df[f] = pd.NA
        cat_keys = set(self.cat_vocab.keys())
        for f in self.feature_names:
            if f not in cat_keys: df[f] = pd.to_numeric(df[f], errors="coerce")
        return df.reindex(columns=self.feature_names)

    def predict(self, user: UserInputL2) -> list[L2PredictResult]:
        processed = preprocess_input_data_L2(user)
        if isinstance(processed, pd.DataFrame) and processed.empty: return []
        X = self._prep_df_for_predict(processed)
        if X.shape[0] == 0: return []

        niter = self.booster.best_iteration or self.booster.current_iteration() or -1
        score = self.booster.predict(X, num_iteration=niter)
        out = processed.copy(); out["score"] = score

        top = (
            out.loc[out["score"] >= self.threshold, ["cand_ma_xet_tuyen", "score"]]
              .assign(cand_ma_xet_tuyen=lambda df: df["cand_ma_xet_tuyen"].astype(str))
              .sort_values("score", ascending=False)
              .drop_duplicates(subset="cand_ma_xet_tuyen", keep="first")
              .reset_index(drop=True)
        )
        result = [L2PredictResult(ma_xet_tuyen=r["cand_ma_xet_tuyen"], score=r["score"]) for _, r in top.iterrows()]
        return discount_fee(user, result)

_CEFR_RE = re.compile(r"\b(A1|A2|B1|B2|C1|C2)\b", re.I)

def _has_cefr(val: str | None, targets: Iterable[str]) -> bool:
    """Kiểm tra 'A2', 'B1'... có xuất hiện (case-insensitive) trong chuỗi."""
    if not val:
        return False
    s = str(val).upper()
    # tìm đúng token CEFR
    m = _CEFR_RE.search(s)
    if m:
        return m.group(1) in {t.upper() for t in targets}
    return any(t.upper() in s for t in targets)

def discount_fee(input: UserInputL2, results: List["L2PredictResult"]) -> List["L2PredictResult"]:
    """
    Giữ lại các kết quả UEF-THPTQG nếu thỏa 1 trong 3 bậc ưu đãi sau:
      - Tier1: (21 ≤ điểm < 24) hoặc CEFR A2, và ngân sách ≥ 60,000,000
      - Tier2: (24 ≤ điểm < 27) hoặc CEFR B1/B2, và ngân sách ≥ 40,000,000
      - Tier3: (27 ≤ điểm ≤ 30) hoặc CEFR C1/C2, và ngân sách ≥ 0
    Các mã khác (không phải UEF…THPTQG) giữ nguyên.
    """
    try:
        score = float(input.diem_chuan)
    except Exception:
        score = 0.0

    try:
        budget = float(input.hoc_phi)
    except Exception:
        budget = 0.0

    out: List["L2PredictResult"] = []
    for r in results:
        code = str(r.ma_xet_tuyen)

        # Chỉ áp dụng rule cho mã UEF...THPTQG
        if code.startswith("UEF") and code.endswith("THPTQG"):
            tier1 = ((21 <= score < 24) or _has_cefr(input.diem_ccta, {"A2"})) and (budget >= 60_000_000)
            tier2 = ((24 <= score < 27) or _has_cefr(input.diem_ccta, {"B1", "B2"})) and (budget >= 40_000_000)
            tier3 = ((27 <= score <= 30) or _has_cefr(input.diem_ccta, {"C1", "C2"})) and (budget >= 0)

            if tier1 or tier2 or tier3:
                out.append(r)
        else:
            out.append(r)
    return out
