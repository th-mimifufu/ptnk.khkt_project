import pandas as pd

from schemas import L2PredictResult, UserInputL2
from utils import preprocess_input_data
import lightgbm as lgb, json, pandas as pd
from pandas.api.types import CategoricalDtype
import os

# Load model once at module level
MODEL_DIR = os.path.join(os.path.dirname(__file__), "../models/user_item_lightgbm")
MODEL_DIR = os.path.abspath(MODEL_DIR)

booster = lgb.Booster(model_file=os.path.join(MODEL_DIR, "l2_lightgbm.txt"))

with open(os.path.join(MODEL_DIR, "feature_names.json"), "r", encoding="utf-8") as f:
    feature_names = json.load(f)
with open(os.path.join(MODEL_DIR, "cat_vocab.json"), "r", encoding="utf-8") as f:
    cat_vocab = json.load(f)

for c, vocab in list(cat_vocab.items()):
    vs = [str(v) for v in vocab if v is not None]
    seen, vs_u = set(), []
    for v in vs:
        if v not in seen:
            seen.add(v); vs_u.append(v)
    if "__UNK__" in vs_u:
        vs_u.remove("__UNK__")
    cat_vocab[c] = ["__UNK__"] + vs_u

def l2_predict_from_input(input_data: UserInputL2, threshold: float = 0.5) -> L2PredictResult:
    """
    Run preprocessing and make a prediction from input data.

    Args:
        input_data (dict): Input data as dictionary (already validated by Pydantic)

    Returns:
        dict: Dictionary of prediction items
    """
    # preprocess_input_data
    processed_data = preprocess_input_data(input_data)
    X = _prep_df_for_predict(processed_data)
    niter = booster.best_iteration or booster.current_iteration() or -1
    score = booster.predict(X, num_iteration=niter)
    out = processed_data.copy()
    out["score"] = score

    top = (
    out.loc[out["score"] >= threshold, ["cand_ma_xet_tuyen", "score"]]
       .assign(cand_ma_xet_tuyen=lambda df: df["cand_ma_xet_tuyen"].astype(str))
       .sort_values("score", ascending=False)
       .drop_duplicates(subset="cand_ma_xet_tuyen", keep="first")
       .reset_index(drop=True)
    )
    top = [L2PredictResult(ma_xet_tuyen=row["cand_ma_xet_tuyen"], score=row["score"]) for _, row in top.iterrows()]
    
    return top


def _prep_df_for_predict(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # ép categories theo vocab + map unseen -> __UNK__
    for c, vocab in cat_vocab.items():
        if c in df.columns:
            s = df[c].astype(str)
            s.loc[~s.isin(vocab)] = "__UNK__"
            df[c] = s.astype(CategoricalDtype(categories=vocab, ordered=False))

    # đảm bảo đủ feature và đúng thứ tự
    for f in feature_names:
        if f not in df.columns:
            df[f] = pd.NA

    # ép numeric cho cột không phải category
    cat_keys = set(cat_vocab.keys())
    for f in feature_names:
        if f not in cat_keys:
            df[f] = pd.to_numeric(df[f], errors="coerce")

    return df.reindex(columns=feature_names)
if __name__ == "__main__":
    # Example usage
    sample_input = UserInputL2(
        tinh_tp="TP. Hồ Chí Minh",
        cong_lap=1,
        to_hop_mon="A00",
        diem_chuan=24.5,
        hoc_phi=20000000,
        ten_ccta="IELTS",
        diem_ccta="6.5",
        hk10=1,
        hk11=1,
        hk12=1,
        hl10=1,
        hl11=1,
        hl12=1,
        nhom_nganh=748
    )
    prediction = l2_predict_from_input(sample_input)
    print(prediction)
