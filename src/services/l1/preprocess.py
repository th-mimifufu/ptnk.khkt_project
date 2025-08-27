import pandas as pd

from src.services.l1.schema import UserInputL1

def preprocess_input_data_L1(data: UserInputL1) -> pd.DataFrame:
    df = pd.DataFrame([data.model_dump()])
    test_df = clean_and_cast_L1(df)
    return test_df

def clean_and_cast_L1(df: pd.DataFrame) -> pd.DataFrame:
    df['hsg_subject'] = df.apply(pick_hsg, axis=1).fillna("0").astype(str)
    for col in ['ahld', 'dan_toc_thieu_so', 'haimuoi_huyen_ngheo_tnb']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

    rows = []
    hsg_df = df[df['hsg_subject'] != "0"].copy()
    hsg_df[['ahld', 'dan_toc_thieu_so', 'haimuoi_huyen_ngheo_tnb']] = 0
    rows.append(hsg_df)

    for col in ['ahld', 'dan_toc_thieu_so', 'haimuoi_huyen_ngheo_tnb']:
        temp_df = df[df[col] == 1].copy()
        temp_df['hsg_subject'] = "0"
        for other_col in ['ahld', 'dan_toc_thieu_so', 'haimuoi_huyen_ngheo_tnb']:
            if other_col != col:
                temp_df[other_col] = 0
        rows.append(temp_df)

    none_df = df[
        (df['hsg_subject'] == "0") &
        (df['ahld'] == 0) &
        (df['dan_toc_thieu_so'] == 0) &
        (df['haimuoi_huyen_ngheo_tnb'] == 0)
    ].copy()
    rows.append(none_df)

    out = pd.concat(rows, ignore_index=True)
    active_cnt = (
        (out['hsg_subject'] != "0").astype(int)
        + out['ahld'] + out['dan_toc_thieu_so'] + out['haimuoi_huyen_ngheo_tnb']
    )
    out = out[active_cnt <= 1].reset_index(drop=True)
    return out

def pick_hsg(row):
    for k in ['hsg_1', 'hsg_2', 'hsg_3']:
        v = row[k]
        if isinstance(v, str) and v.strip() and v != '0':
            return v.strip()
        if isinstance(v, (int, float)) and v != 0:
            return str(v)
    return "0"