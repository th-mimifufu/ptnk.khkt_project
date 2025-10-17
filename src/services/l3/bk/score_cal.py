# from typing import List, Tuple, Any
# from src.services.l3.spk.constants import SUBJECT_MAP, AWARD_QG_POINTS, AWARD_ENGLISH_POINTS
# from src.services.l3.spk.schema import HocBa, AwardQG, AwardEnglish, DGNL
# import pandas as pd

# def hoc_ba_get_dtbm(hoc_ba: HocBa, subject: str) -> float:
#     """
#     Tính điểm trung bình môn từ học bạ 3 năm
    
#     Args:
#         hoc_ba: HocBa object
#         subject: Tên môn (Toán, Lý, Hóa, ...)
        
#     Returns:
#         Điểm trung bình môn
#     """
#     field_name = SUBJECT_MAP.get(subject, subject.lower())
#     scores = []
#     for grade in [hoc_ba.grade_10, hoc_ba.grade_11, hoc_ba.grade_12]:
#         score = getattr(grade, field_name, None)
#         if score is not None:
#             scores.append(score)
    
#     return sum(scores) / len(scores) if scores else 0.0

# # def english_convert(level: str) -> str:
# #     """QUY ĐỔI CHỨNG CHỈ TIẾNG ANH

# #     Thí sinh có chứng chỉ sẽ được quy đổi sang điểm tương ứng của môn tiếng Anh trong điểm thi tốt nghiệp THPT và học bạ THPT đối với các tổ hợp xét tuyển có dùng môn tiếng Anh """
# #     mapping = {
# #         "0": -1,
# #         "A1": -1,
# #         "A2": -1,
# #         "B1": 8.0,
# #         "B2": 8.5,
# #         "C1": 10.0,
# #         "C2": 10.0
# #     }
# #     return mapping.get(level, -1)

# def hoc_ba_calculate_to_hop_score(hoc_ba: Any, to_hop: List[str], english_cer: AwardEnglish) -> float:
#     """
#     Tính điểm cho một tổ hợp môn
#     Công thức: (môn_đầu_tiên + môn_thứ_hai + môn_thứ_ba) / 3

#     Args:
#         hoc_ba: HocBa object
#         to_hop: List 3 môn trong tổ hợp
        
#     Returns:
#         Điểm tổ hợp
#     """
#     if len(to_hop) != 3:
#         return 0.0

#     dtbm_scores = []
#     for mon in to_hop:
#         if mon == "Anh":
#             english_score = AWARD_ENGLISH_POINTS.get(english_cer.level, -1)
#             if english_score == -1:
#                 # Nếu không tìm thấy level, dùng điểm trung bình môn Anh từ học bạ
#                 dtbm_scores.append(hoc_ba_get_dtbm(hoc_ba, "Anh"))
#             else:
#                 dtbm_scores.append(english_score)
#         else:
#             dtbm_scores.append(hoc_ba_get_dtbm(hoc_ba, mon))
#     weighted_score = (dtbm_scores[0] + dtbm_scores[1] + dtbm_scores[2])
#     return weighted_score / 3

# def hoc_ba_calculate_best_to_hop_score(hoc_ba: Any, to_hop_list: List[List[str]]) -> Tuple[float, List[str]]:
#     """
#     Tính điểm cho tất cả tổ hợp và trả về tổ hợp có điểm cao nhất
    
#     Args:
#         hoc_ba: HocBa object
#         to_hop_list: List các tổ hợp môn. ví dụ: [['Toán', 'Lý', 'Hóa'], ['Toán', 'Anh', 'Văn'], ...]
        
#     Returns:
#         Tuple (điểm_cao_nhất, tổ_hợp_tốt_nhất)
#     """
#     if not to_hop_list:
#         return 0.0, []
    
#     best_score = 0.0
#     best_to_hop = []
    
#     for to_hop in to_hop_list:
#         score = hoc_ba_calculate_to_hop_score(hoc_ba, to_hop)
#         if score > best_score:
#             best_score = score
#             best_to_hop = to_hop
    
#     return best_score, best_to_hop

# # def is_eligible_for_geography_bonus(ma_nganh: str) -> bool:
# #     """Kiểm tra ngành có được cộng điểm giải Địa lý không"""
# #     geography_eligible_codes = [
# #         "7440201_NN",  # Nhóm ngành Địa chất học
# #         "7440228",  # Hải dương học  
# #         "7440301",  # Khoa học Môi trường
# #         "7440301_DKD",  # Khoa học Môi trường (CT tăng cường tiếng Anh)
# #         "7510406",  # Công nghệ Kỹ thuật Môi trường
# #         "7520501",  # Kỹ thuật địa chất
# #         "7850101"   # Quản lý tài nguyên và môi trường
# #     ]
    
# #     # Kiểm tra mã ngành có trong danh sách không
# #     for code in geography_eligible_codes:
# #         if ma_nganh.startswith(code):
# #             return True
    
# #     return False

# # def is_english_enhanced_program(ma_nganh: str) -> bool:
# #     """Kiểm tra có phải chương trình tăng cường tiếng Anh không"""
# #     english_enhanced_codes = [
# #         "7420101_DKD",  # Sinh học
# #         "7420201_DKD",  # Công nghệ sinh học
# #         "7440102_DKD",  # Vật lý học
# #         "7440112_DKD",  # Hóa học
# #         "7440301_DKD",  # Khoa học môi trường
# #         "7510401_DKD",  # Công nghệ kỹ thuật hóa học
# #         "7520207_DKD",  # Kỹ thuật điện tử, viễn thông
# #         "7440122_DKD",  # Khoa học vật liệu
# #         "7480201_DKD",  # Công nghệ thông tin
# #         "7480101_TT"    # Khoa học máy tính
# #     ]
    
#     # return ma_nganh in english_enhanced_codes

# # def is_it_advanced_program(ma_nganh: str) -> bool:
# #     """Kiểm tra có phải chương trình đề án CNTT không"""
# #     it_advanced_codes = [
# #         "7480201_DKD",  # Công nghệ thông tin (CT tăng cường tiếng Anh)
# #         "7480101_TT"    # Khoa học máy tính (CT tiên tiến)
# #     ]
    
# #     return ma_nganh in it_advanced_codes

# # def calculate_bonus(award_qg: Any, award_english: Any, ma_nganh: str) -> float:
# #     """
# #     Tính điểm thưởng từ giải quốc gia và chứng chỉ tiếng Anh
    
# #     Args:
# #         award_qg: AwardQG object hoặc None
# #         award_english: AwardEnglish object hoặc None  
# #         ma_nganh: Mã ngành
        
# #     Returns:
# #         Tổng điểm thưởng
# #     """
# #     bonus = 0.0
    
# #     # Điểm thưởng giải quốc gia
# #     if award_qg and hasattr(award_qg, 'level') and hasattr(award_qg, 'subject'):
# #         subject = award_qg.subject
# #         level = award_qg.level
        
# #         # Các môn được cộng điểm cho tất cả ngành
# #         general_subjects = ["Toán", "Lý", "Hóa", "Sinh", "Tin", "Anh"]

# #         if subject in general_subjects:
# #             bonus += AWARD_QG_POINTS.get(level, 0.0)
# #         elif subject == "Địa" and is_eligible_for_geography_bonus(ma_nganh):
# #             # Giải Địa chỉ cộng cho một số ngành cụ thể
# #             bonus += AWARD_QG_POINTS.get(level, 0.0)
# #     return bonus

# def parse_to_hop_from_dataframe(df_to_hop: pd.DataFrame, ma_nganh: str) -> List[List[str]]:
#     """
#     Parse DataFrame tổ hợp môn thành List[List[str]]
    
#     Args:
#         df_to_hop: DataFrame với columns ['nganh', 'Tổ hợp môn']
#         ma_nganh: Mã ngành cần lấy tổ hợp
        
#     Returns:
#         List[List[str]]: [["Toán", "Lý", "Hóa"], ["Toán", "Hóa", "Anh"], ...]
#     """
#     # Lọc các dòng cho ngành này
#     nganh_rows = df_to_hop[df_to_hop['nganh'] == ma_nganh]
    
#     to_hop_list = []
    
#     for _, row in nganh_rows.iterrows():
#         to_hop_str = row['Tổ hợp môn']
        
#         # Parse "(Toán, Lý, Hoá)" -> ["Toán", "Lý", "Hoá"]
#         if isinstance(to_hop_str, str):
#             # Loại bỏ dấu ngoặc
#             clean_str = to_hop_str.strip("()")
#             # Split và clean whitespace
#             subjects = [s.strip() for s in clean_str.split(",")]
            
#             # Đảm bảo có đủ 3 môn
#             if len(subjects) == 3:
#                 to_hop_list.append(subjects)
    
#     return to_hop_list

# def thpt_calculate_scores(user_input: Any, df_schools: pd.DataFrame) -> pd.DataFrame:
#     """
#     Tính điểm học bạ cho các ngành trong df_schools dựa trên user_input

#     Args:
#         user_input: UserInputL3 object
#         df_schools: DataFrame với các ngành cần tính điểm. Cần có columns ['ma_nganh', 'to_hop_mon', 'diem_chuan']

#     Returns:
#         DataFrame với thêm các cột ['to_hop_list', 'best_to_hop', 'best_to_hop_score', 'bonus_points', 'total_score']
#     """
#     # Bước 1: Lọc trường theo yêu cầu
#     filtered_schools = filter_schools(df_schools, user_input)

#     if filtered_schools.empty:
#         return pd.DataFrame()

#     # Bước 2: Lấy tổ hợp môn từ database
#     ma_nganh_list = filtered_schools['ma_nganh'].tolist()
#     to_hop_data = get_to_hop_mon_from_db(ma_nganh_list)
#     print(to_hop_data)
#     # Bước 3: Tính điểm học bạ cho từng ngành
#     results = []

#     for _, row in filtered_schools.iterrows():
#         ma_nganh = row['ma_nganh']
#         print(f"Ngành: {ma_nganh}")
#         to_hop_list = parse_to_hop_from_dataframe(to_hop_data, ma_nganh)
#         print(f"Tổ hợp: {to_hop_list}")
#         if not to_hop_list:
#             continue

#         # Tính điểm tổ hợp tốt nhất
#         best_score, best_to_hop = hoc_ba_calculate_best_to_hop_score(user_input.hoc_ba, to_hop_list)
#         print(f"Ngành {ma_nganh}, Tổ hợp {best_to_hop}, Điểm {best_score}")
#         # Tính điểm thưởng
#         bonus = calculate_bonus(user_input.award_qg, user_input.award_english, ma_nganh)

#         # Tổng điểm
#         total_score = best_score + bonus

#         # Thêm vào kết quả
#         result_row = row.to_dict()
#         result_row.update({
#             'to_hop_list': to_hop_list,
#             'best_to_hop': best_to_hop,
#             'best_to_hop_score': round(best_score, 2),
#             'bonus_points': round(bonus, 2),
#             'total_score': round(total_score, 2)
#         })
#         results.append(result_row)

#     return pd.DataFrame(results)

# def bk_fomula(diem_hoc_luc: float, diem_cong: float=0.0, diem_uu_tien: float=0.0) -> float:
#     """
#     Tính điểm xét tuyển theo công thức:
#     - Điểm xét tuyển = Điểm học lực + Điểm cộng + Điểm ưu tiên (thang 100).
#     - Điểm cộng tối đa 10 điểm (nếu tổng > 100 thì lấy 100 - Điểm học lực).
#     - Điểm ưu tiên: nếu tổng < 75 thì lấy nguyên, nếu >= 75 thì giảm dần theo công thức.
#     Args:
#         diem_hoc_luc: Điểm học lực
#         diem_cong: Điểm cộng
#         diem_uu_tien: Điểm ưu tiên
#     Returns:
#         Điểm xét tuyển (thang 10, làm tròn 2 chữ số)
#     """
#     # Quy đổi điểm học lực, điểm cộng, điểm ưu tiên về thang 100
#     diem_hoc_luc_100 = diem_hoc_luc * 10
#     diem_cong_100 = diem_cong * 10
#     diem_uu_tien_100 = diem_uu_tien / 3 * 10  # Điểm ưu tiên quy đổi, tối đa 9.17

#     # Tính điểm cộng thành tích (không vượt quá 10)
#     if diem_hoc_luc_100 + diem_cong_100 < 100:
#         diem_cong_final = min(diem_cong_100, 10)
#     else:
#         diem_cong_final = max(0, 100 - diem_hoc_luc_100)

#     # Tính điểm ưu tiên
#     if diem_hoc_luc_100 + diem_cong_final < 75:
#         diem_uu_tien_final = diem_uu_tien_100
#     else:
#         diem_uu_tien_final = ((100 - diem_hoc_luc_100 - diem_cong_final) / 25) * diem_uu_tien_100
#         diem_uu_tien_final = round(max(0, diem_uu_tien_final), 2)

#     # Tổng điểm xét tuyển (thang 100)
#     diem_xet_tuyen_100 = diem_hoc_luc_100 + diem_cong_final + diem_uu_tien_final

#     # Quy đổi về thang 10
#     diem_xet_tuyen_10 = diem_xet_tuyen_100 / 10
#     return round(diem_xet_tuyen_10, 2)
#     if thpt_score < 0 or thpt_score > 10 or dgnl_score < 0 or dgnl_score > 120:
#         return 0.0
    
#     # Chuẩn hoá điểm đánh giá năng lực về thang điểm 10
#     dgnl_normalized = (dgnl_score / 120) * 10
    
#     total_score = (0.7 * thpt_score) + (0.3 * dgnl_normalized)
#     return total_score
#             'best_to_hop_score': round(best_score, 2),
#             'bonus_points': round(bonus, 2),
#             'total_score': round(total_score, 2)
#         })
#         results.append(result_row)