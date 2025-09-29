from typing import Dict, List
import pandas as pd
from src.services.l3.schema import UserInputL3

def filter_schools(df_schools: pd.DataFrame, user_input: UserInputL3) -> pd.DataFrame:
    """
    Lọc danh sách trường-ngành theo điều kiện user
    
    Args:
        df_schools: DataFrame với columns ['cong_lap', 'tinh_tp', 'hoc_phi', 'nhom_nganh', 'ten_truong', 'ma_nganh']
        user_input: UserInputL3 object
        
    Returns:
        DataFrame đã lọc
    """
    filtered_df = df_schools.copy()

    # Lọc theo công lập/tư thục
    filtered_df = filtered_df[filtered_df['cong_lap'] == user_input.cong_lap]
    
    # Lọc theo tỉnh/thành phố
    if user_input.tinh_tp:
        filtered_df = filtered_df[filtered_df['tp'] == user_input.tinh_tp]
    
    # Lọc theo học phí (nhỏ hơn hoặc bằng ngân sách dự kiến)
    if user_input.hoc_phi:
        filtered_df = filtered_df[filtered_df['Học phí'] <= user_input.hoc_phi]
    
    # Lọc theo nhóm ngành
    filtered_df = filtered_df[filtered_df['nhom_nganh'] == user_input.nhom_nganh.value]
    
    return filtered_df

def get_to_hop_mon_from_db(ma_nganh_list: List[str]) -> pd.DataFrame:
    """
    Query database để lấy tổ hợp môn cho các ngành
    
    Args:
        ma_nganh_list: List mã ngành cần lấy tổ hợp
        
    Returns:
        Dict {ma_nganh: [[to_hop_1], [to_hop_2], ...]}
    """
    
    df = pd.read_excel("data/spk_hb_thm.xlsx")
    df = df[df['nganh'].isin(ma_nganh_list)]

    return df
