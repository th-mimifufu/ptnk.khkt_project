import os
import re
import numpy as np
import pandas as pd
import polars as pl

from src.services.l2.schema import UserInputL2
from src.core.config import settings

def preprocess_input_data_L2(data: UserInputL2) -> pd.DataFrame:
    df = pd.DataFrame([data.model_dump()])
    l2_uni = pd.read_excel(os.path.join(settings.DATA_DIR, "L2_uni_requirement.xlsx")).astype(str)
    l2_uni = pl.from_pandas(l2_uni).with_columns([
        pl.col("cong_lap").cast(pl.Int64),
        pl.col("tinh_tp").cast(pl.Utf8),
        pl.col("to_hop_mon").cast(pl.Utf8),
        pl.col("diem_chuan").cast(pl.Float64),
        pl.col("hoc_phi").cast(pl.Int64),
        pl.col("ten_ccta").cast(pl.Utf8),
        pl.col("diem_ccta").cast(pl.Utf8),
        pl.col("diem_quy_doi").cast(pl.Float64),
        pl.col("hk10").cast(pl.Int64),
        pl.col("hk11").cast(pl.Int64),
        pl.col("hk12").cast(pl.Int64),
        pl.col("hl10").cast(pl.Int64),
        pl.col("hl11").cast(pl.Int64),
        pl.col("hl12").cast(pl.Float64),
        pl.col("nhom_nganh").cast(pl.Int64),
        pl.col("ma_xet_tuyen").cast(pl.Utf8)
    ])
    test_df = input_to_pairs_L2(pl.from_pandas(df), l2_uni)
    return test_df

def input_to_pairs_L2(input_data: pl.DataFrame, candidate_list: pl.DataFrame) -> pd.DataFrame:
    cand_tp = input_data['tinh_tp'].unique().to_list()
    cand_thm = input_data['to_hop_mon'].unique().to_list()
    cand_cl = input_data['cong_lap'].unique().to_list()
    cand_nn = input_data['nhom_nganh'].unique().to_list()
    candidate_uni_pl = candidate_list.filter(
        pl.col('tinh_tp').is_in(cand_tp) &
        pl.col('to_hop_mon').is_in(cand_thm) &
        pl.col('cong_lap').is_in(cand_cl) &
        pl.col('nhom_nganh').is_in(cand_nn)
    ).clone()

    student_info_pd = input_data.to_pandas()
    candidate_uni_pd = candidate_uni_pl.to_pandas()
    return filter_candidates_per_student_L2(student_info_pd, candidate_uni_pd)

def filter_candidates_per_student_L2(
    student_df: pd.DataFrame,
    candidate_df: pd.DataFrame,
    hard_filters=None,
) -> pd.DataFrame:
    hard_filters = ['tinh_tp', 'to_hop_mon', 'cong_lap', 'nhom_nganh']
    HB = ['hk10', 'hk11', 'hk12', 'hl10', 'hl11', 'hl12']
    outs = []

    for _, s in student_df.iterrows():
        cand = candidate_df.copy()
        for k in hard_filters:
            if k in cand.columns and k in s.index and pd.notna(s[k]):
                cand = cand[cand[k] == s[k]]

        stu_score = pd.to_numeric(s.get('diem_chuan', np.nan), errors='coerce')
        cand['student_diem_chuan'] = float(stu_score) if pd.notna(stu_score) else np.nan

        budget = pd.to_numeric(s.get('hoc_phi', np.nan), errors='coerce')
        cand['student_budget_max'] = 0 if pd.isna(budget) else int(budget)

        for k in ['cong_lap', 'tinh_tp', 'to_hop_mon', 'ten_ccta', 'diem_ccta', 'nhom_nganh']:
            cand[f'student_{k}'] = s.get(k, pd.NA)

        cand['cand_diem_chuan_final'] = pd.to_numeric(cand.get('diem_chuan_final'), errors='coerce')
        cand['cand_hoc_phi'] = pd.to_numeric(cand.get('hoc_phi'), errors='coerce').fillna(0).astype('int64')

        if 'y_base' in cand.columns:
            cand['cand_y_base'] = pd.to_numeric(cand['y_base'], errors='coerce')
        elif 'diem_chuan' in cand.columns:
            cand['cand_y_base'] = pd.to_numeric(cand['diem_chuan'], errors='coerce')
        else:
            cand['cand_y_base'] = cand['cand_diem_chuan_final']

        for k in ['cong_lap', 'tinh_tp', 'to_hop_mon', 'nhom_nganh', 'ma_xet_tuyen']:
            cand[f'cand_{k}'] = cand.get(k, pd.NA)

        cand['cand_is_base_row'] = cand.get('is_base_row', False)

        stu_hb_vals = {}
        for c in HB:
            val = s.get(c, np.nan)
            sv = 10 if pd.isna(val) else float(re.search(r'(\d+\.?\d*)', str(val)).group(1)) if re.search(r'(\d+\.?\d*)', str(val)) else 10
            if pd.isna(sv) or sv == 0: sv = 10
            stu_hb_vals[c] = int(sv)

        for c in HB:
            if c in cand.columns:
                v = cand[c].astype(str).str.extract(r'(\d+\.?\d*)')[0].astype(float)
                v = v.fillna(10).replace(0, 10).astype('int64')
            else:
                v = pd.Series(10, index=cand.index, dtype='int64')
            cand[f'diff_{c}'] = (v - stu_hb_vals[c]).astype('int64')

        cols_num = [
            'student_diem_chuan', 'student_budget_max',
            'cand_diem_chuan_final', 'cand_hoc_phi', 'cand_y_base',
            'diff_hk10', 'diff_hk11', 'diff_hk12', 'diff_hl10', 'diff_hl11', 'diff_hl12'
        ]
        cols_cat = [
            'student_cong_lap', 'student_tinh_tp', 'student_to_hop_mon', 'student_ten_ccta', 'student_diem_ccta', 'student_nhom_nganh',
            'cand_cong_lap', 'cand_tinh_tp', 'cand_to_hop_mon', 'cand_nhom_nganh', 'cand_ma_xet_tuyen', 'cand_is_base_row'
        ]
        need_cols = cols_num + cols_cat
        for c in need_cols:
            if c not in cand.columns:
                cand[c] = pd.NA

        out = cand[need_cols].copy()
        outs.append(out)

    test_df = pd.concat(outs, ignore_index=True)

    for c in ['student_diem_chuan', 'cand_diem_chuan_final', 'cand_y_base']:
        test_df[c] = pd.to_numeric(test_df[c], errors='coerce').astype('float64')
    for c in ['student_budget_max', 'cand_hoc_phi', 'diff_hk10', 'diff_hk11', 'diff_hk12', 'diff_hl10', 'diff_hl11', 'diff_hl12']:
        test_df[c] = pd.to_numeric(test_df[c], errors='coerce').fillna(0).astype('int64')
    for c in cols_cat:
        test_df[c] = test_df[c].astype('category')
    return test_df
