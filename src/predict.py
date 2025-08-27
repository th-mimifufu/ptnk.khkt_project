# from typing import List
# import numpy as np
# import pandas as pd
# import lightgbm as lgb
# import json
# import os
# import joblib
# from pandas.api.types import CategoricalDtype

# from schemas import L2PredictResult, UserInputL2, UserInputL1, L1PredictResult
# from utils import preprocess_input_data_L1, preprocess_input_data_L2

# # -------------------- Constants & Model Loading --------------------
# MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../models"))

# # L2 Model
# booster = lgb.Booster(model_file=os.path.join(MODEL_DIR, "user_item_lightgbm/l2_lightgbm.txt"))
# with open(os.path.join(MODEL_DIR, "user_item_lightgbm/feature_names.json"), "r", encoding="utf-8") as f:
#     feature_names = json.load(f)
# with open(os.path.join(MODEL_DIR, "user_item_lightgbm/cat_vocab.json"), "r", encoding="utf-8") as f:
#     cat_vocab = json.load(f)

# # Clean category vocabularies
# for c, vocab in cat_vocab.items():
#     vs = [str(v) for v in vocab if v is not None]
#     seen, vs_u = set(), []
#     for v in vs:
#         if v not in seen:
#             seen.add(v)
#             vs_u.append(v)
#     if "__UNK__" in vs_u:
#         vs_u.remove("__UNK__")
#     cat_vocab[c] = ["__UNK__"] + vs_u

# # L1 Model
# bundle = joblib.load(os.path.join(MODEL_DIR, "l1_model.joblib"))
# models = bundle["models"]
# encoders = bundle["encoders"]
# label_encoders = bundle["label_encoders"]
# class_lists = bundle["class_lists"]
# meta = bundle["meta"]
# group_cols = meta["group_cols"]
# ohe_cols = meta["ohe_cols"]

# # -------------------- L2 Prediction --------------------
# def l2_predict_from_input(input_data: UserInputL2, threshold: float = 0.5) -> List[L2PredictResult]:
#     processed_data = preprocess_input_data_L2(input_data)
#     X = _prep_df_for_predict(processed_data)
#     niter = booster.best_iteration or booster.current_iteration() or -1
#     score = booster.predict(X, num_iteration=niter)
#     out = processed_data.copy()
#     out["score"] = score

#     top = (
#         out.loc[out["score"] >= threshold, ["cand_ma_xet_tuyen", "score"]]
#         .assign(cand_ma_xet_tuyen=lambda df: df["cand_ma_xet_tuyen"].astype(str))
#         .sort_values("score", ascending=False)
#         .drop_duplicates(subset="cand_ma_xet_tuyen", keep="first")
#         .reset_index(drop=True)
#     )
#     return [
#         L2PredictResult(ma_xet_tuyen=row["cand_ma_xet_tuyen"], score=row["score"])
#         for _, row in top.iterrows()
#     ]

# def _prep_df_for_predict(df: pd.DataFrame) -> pd.DataFrame:
#     df = df.copy()
#     # Map categories and unseen values
#     for c, vocab in cat_vocab.items():
#         if c in df.columns:
#             s = df[c].astype(str)
#             s.loc[~s.isin(vocab)] = "__UNK__"
#             df[c] = s.astype(CategoricalDtype(categories=vocab, ordered=False))
#     # Ensure all features exist
#     for f in feature_names:
#         if f not in df.columns:
#             df[f] = pd.NA
#     # Convert non-category columns to numeric
#     cat_keys = set(cat_vocab.keys())
#     for f in feature_names:
#         if f not in cat_keys:
#             df[f] = pd.to_numeric(df[f], errors="coerce")
#     return df.reindex(columns=feature_names)

# # -------------------- L1 Prediction --------------------
# def l1_predict_from_input(input_data: UserInputL1) -> List[L1PredictResult]:
#     processed_data = preprocess_input_data_L1(input_data).reset_index(drop=True)
#     processed_data = processed_data.assign(row_id=lambda d: d.index)
#     results: List[L1PredictResult] = []

#     for _, r in processed_data.iterrows():
#         gkey = tuple(r[c] for c in group_cols)
#         loai = infer_loai_uu_tien(r)
#         if loai == "Không ưu tiên":
#             results.append(L1PredictResult(loai_uu_tien=loai, ma_xet_tuyen={}))
#             continue
#         if gkey not in models:
#             results.append(L1PredictResult(loai_uu_tien=loai, ma_xet_tuyen={}))
#             continue
#         clf = models[gkey]
#         enc = encoders[gkey]
#         le = label_encoders[gkey]
#         cls = class_lists[gkey]
#         if clf is None:
#             results.append(L1PredictResult(loai_uu_tien=loai, ma_xet_tuyen={cls[0]: 1.0}))
#             continue
#         feat_in = list(enc.feature_names_in_) if hasattr(enc, 'feature_names_in_') and enc.feature_names_in_ is not None else ohe_cols

#         x_df = r[feat_in].astype(str).to_frame().T
#         X = enc.transform(x_df)
#         if hasattr(clf, "predict_proba"):
#             p = clf.predict_proba(X)[0]
#             if p.sum() <= 0:
#                 results.append(L1PredictResult(loai_uu_tien=loai, ma_xet_tuyen={}))
#                 continue
#             order = np.argsort(p)[::-1]
#             labels_sorted = le.classes_[order]
#             probs_sorted = (p[order] / p.sum()).astype(float)
#             out_map = {lab: float(pr) for lab, pr in zip(labels_sorted, probs_sorted)}
#             results.append(L1PredictResult(loai_uu_tien=loai, ma_xet_tuyen=out_map))
#         else:
#             yhat = clf.predict(X)[0]
#             pred = le.inverse_transform([yhat])[0]
#             results.append(L1PredictResult(loai_uu_tien=loai, ma_xet_tuyen={pred: 1.0}))
#     return results

# def infer_loai_uu_tien(row) -> str:
#     subj = str(row.get('hsg_subject', '0'))
#     if subj not in ('0', 'UNK', 'None', 'nan', ''):
#         return f"HSG {subj}"
#     if int(row.get('ahld', 0)) == 1:
#         return "AHLD"
#     if int(row.get('dan_toc_thieu_so', 0)) == 1:
#         return "Dân tộc thiểu số"
#     if int(row.get('haimuoi_huyen_ngheo_tnb', 0)) == 1:
#         return "50 huyện nghèo/TNB"
#     return "Không ưu tiên"

# # -------------------- Example Usage --------------------
# if __name__ == "__main__":
#     sample_input = UserInputL1(
#         cong_lap=1,
#         tinh_tp="TP. Hồ Chí Minh",
#         hoc_phi=20000000,
#         hsg_1="Toán",
#         hsg_2="0",
#         hsg_3="0",
#         ahld="1",
#         dan_toc_thieu_so="0",
#         haimuoi_huyen_ngheo_tnb="0",
#         nhom_nganh=748
#     )
#     prediction = l1_predict_from_input(sample_input)
#     print(prediction)
