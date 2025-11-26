from enum import IntEnum, StrEnum, Enum
from types import MappingProxyType

class VietnameseSubject(StrEnum):
    TOAN = "Toán"
    VAN = "Văn"
    TIENG_ANH = "Anh"
    VAT_LY = "Lý"
    HOA_HOC = "Hoá"
    SINH = "Sinh"
    SU = "Sử"
    DIA = "Địa"
    TIN = "Tin"
    TIENG_PHAP = "Tiếng Pháp"
    TIENG_TRUNG = "Tiếng Trung"
    TIENG_NHAT = "Tiếng Nhật"
    TIENG_NGA = "Tiếng Nga"
    TIENG_HAN = "Tiếng Hàn"
    TIENG_DUC = "Tiếng Đức"
    GDKT_PL = "GDKT&PL"
    KHOA_HOC_TU_NHIEN = "Khoa học tự nhiên"
    KHOA_HOC_XA_HOI = "Khoa học xã hội"
    CONG_NGHE_CONG_NGHIEP = "Công nghệ công nghiệp"
    CONG_NGHE_NONG_NGHIEP = "Công nghệ nông nghiệp"
    NANG_KHIEU_VE_1 = "Năng khiếu vẽ 1"
    NANG_KHIEU_VE_2 = "Năng khiếu vẽ 2"
    VE_MY_THUAT = "Vẽ mỹ thuật"
    VE_HINH_HOA_MY_THUAT = "Vẽ hình họa mỹ thuật"
    VE_TRANG_TRI_MAU = "Vẽ trang trí màu"
    VE_NANG_KHIEU = "Vẽ năng khiếu"
    VE_HINH_HOA = "Vẽ hình họa"
    VE_TRANG_TRI = "Vẽ trang trí"
    DOC_HIEU = "Đọc hiểu"
    TU_DUY_GIAI_QUYET_NGU_VAN_DE = "Tư duy giải quyết ngữ văn đề"
    DOC_DIEN_CAM = "Đọc diễn cảm"
    HAT = "Hát"
    HAT_MUA = "Hát múa"
    NANG_KHIEU = "Năng khiếu"
    NANG_KHIEU_1 = "Năng khiếu 1"
    NANG_KHIEU_2 = "Năng khiếu 2"
    NANG_KHIEU_MAM_NON = "Năng khiếu mầm non"
    NANG_KHIEU_MAM_NON_1 = "Năng khiếu mầm non 1"
    NANG_KHIEU_MAM_NON_2 = "Năng khiếu mầm non 2"
    NANG_KHIEU_AM_NHAC_1 = "Năng khiếu âm nhạc 1"
    NANG_KHIEU_AM_NHAC_2 = "Năng khiếu âm nhạc 2"
    HAT_XUONG_AM = "Hát xướng âm"
    BIEU_DIEN_NGHE_THUAT = "Biểu diễn nghệ thuật"
    KY_XUONG_AM = "Ký xướng âm"
    HAT_BIEU_DIEN_NHAC_CU = "Hát biểu diễn nhạc cụ"
    CHUYEN_MON_AM_NHAC = "Chuyên môn âm nhạc"
    CHUYEN_MON_AM_NHAC_1 = "Chuyên môn âm nhạc 1"
    CHUYEN_MON_AM_NHAC_2 = "Chuyên môn âm nhạc 2"
    GHI_AM_XUONG_AM = "Ghi âm xướng âm"
    HOA_THANH = "Hòa thanh"
    PHAT_TRIEN_CHU_DE_PHO_THO = "Phát triển chủ đề / phổ thơ"
    CHI_HUY_TAI_CHO = "Chỉ huy tại chỗ"
    NANG_KHIEU_THUYET_TRINH = "Năng khiếu thuyết trình"
    XAY_DUNG_KICH_BAN_SU_KIEN = "Xây dựng kịch bản sự kiện"
    NANG_KHIEU_BAO_CHI = "Năng khiếu báo chí"
    NANG_KHIEU_ANH_BAO_CHI = "Năng khiếu ảnh báo chí"
    NANG_KHIEU_BIEU_DIEN_NGHE_THUAT = "Năng khiếu biểu diễn nghệ thuật"
    NANG_KHIEU_KIEN_THUC_VAN_HOA_XA_HOI_NGHE_THUAT = "Năng khiếu kiến thức văn hóa xã hội - nghệ thuật"
    NANG_KHIEU_QUAY_PHIM_TRUYEN_HINH = "Năng khiếu quay phim truyền hình"
    CHUNG_CHI_QUY_DOI_TIENG_ANH = "Chứng chỉ quy đổi tiếng Anh"
    NANG_KHIEU_SKDA_1 = "Năng khiếu sân khấu điện ảnh 1"
    NANG_KHIEU_SKDA_2 = "Năng khiếu sân khấu điện ảnh 2"
    NANG_KHIEU_TDTT = "Năng khiếu thể dục thể thao"

SUBJECT_GROUPS = MappingProxyType({
    # Khối A
    "A00": [
        VietnameseSubject.TOAN,
        VietnameseSubject.VAT_LY,
        VietnameseSubject.HOA_HOC,
    ],
    "A01": [
        VietnameseSubject.TOAN,
        VietnameseSubject.VAT_LY,
        VietnameseSubject.TIENG_ANH,
    ],
    "A02": [
        VietnameseSubject.TOAN,
        VietnameseSubject.VAT_LY,
        VietnameseSubject.SINH,
    ],
    "A03": [
        VietnameseSubject.TOAN,
        VietnameseSubject.VAT_LY,
        VietnameseSubject.SU,
    ],
    "A04": [
        VietnameseSubject.TOAN,
        VietnameseSubject.VAT_LY,
        VietnameseSubject.DIA,
    ],
    "A05": [
        VietnameseSubject.TOAN,
        VietnameseSubject.HOA_HOC,
        VietnameseSubject.SU,
    ],
    "A06": [
        VietnameseSubject.TOAN,
        VietnameseSubject.HOA_HOC,
        VietnameseSubject.DIA,
    ],
    "A07": [
        VietnameseSubject.TOAN,
        VietnameseSubject.SU,
        VietnameseSubject.DIA,
    ],
    "A08": [
        VietnameseSubject.TOAN,
        VietnameseSubject.SU,
        VietnameseSubject.GDKT_PL,
    ],
    "A09": [
        VietnameseSubject.TOAN,
        VietnameseSubject.DIA,
        VietnameseSubject.GDKT_PL,
    ],
    "A10": [
        VietnameseSubject.TOAN,
        VietnameseSubject.VAT_LY,
        VietnameseSubject.GDKT_PL,
    ],
    "A11": [
        VietnameseSubject.TOAN,
        VietnameseSubject.HOA_HOC,
        VietnameseSubject.GDKT_PL,
    ],
    "A12": [
        VietnameseSubject.TOAN,
        VietnameseSubject.KHOA_HOC_TU_NHIEN,
        VietnameseSubject.KHOA_HOC_XA_HOI,
    ],
    "A14": [
        VietnameseSubject.TOAN,
        VietnameseSubject.KHOA_HOC_TU_NHIEN,
        VietnameseSubject.DIA,
    ],
    "A15": [
        VietnameseSubject.TOAN,
        VietnameseSubject.KHOA_HOC_TU_NHIEN,
        VietnameseSubject.GDKT_PL,
    ],
    "A16": [
        VietnameseSubject.TOAN,
        VietnameseSubject.KHOA_HOC_TU_NHIEN,
        VietnameseSubject.VAN,
    ],
    "A17": [
        VietnameseSubject.TOAN,
        VietnameseSubject.KHOA_HOC_XA_HOI,
        VietnameseSubject.VAT_LY,
    ],
    "A18": [
        VietnameseSubject.TOAN,
        VietnameseSubject.KHOA_HOC_XA_HOI,
        VietnameseSubject.HOA_HOC,
    ],

    # Khối B
    "B00": [
        VietnameseSubject.TOAN,
        VietnameseSubject.HOA_HOC,
        VietnameseSubject.SINH,
    ],
    "B01": [
        VietnameseSubject.TOAN,
        VietnameseSubject.SINH,
        VietnameseSubject.SU,
    ],
    "B02": [
        VietnameseSubject.TOAN,
        VietnameseSubject.SINH,
        VietnameseSubject.DIA,
    ],
    "B03": [
        VietnameseSubject.TOAN,
        VietnameseSubject.SINH,
        VietnameseSubject.VAN,
    ],
    "B04": [
        VietnameseSubject.TOAN,
        VietnameseSubject.SINH,
        VietnameseSubject.GDKT_PL,
    ],
    "B05": [
        VietnameseSubject.TOAN,
        VietnameseSubject.SINH,
        VietnameseSubject.KHOA_HOC_XA_HOI,
    ],
    "B08": [
        VietnameseSubject.TOAN,
        VietnameseSubject.SINH,
        VietnameseSubject.TIENG_ANH,
    ],

    # Khối C
    "C00": [
        VietnameseSubject.VAN,
        VietnameseSubject.SU,
        VietnameseSubject.DIA,
    ],
    "C01": [
        VietnameseSubject.VAN,
        VietnameseSubject.TOAN,
        VietnameseSubject.VAT_LY,
    ],
    "C02": [
        VietnameseSubject.VAN,
        VietnameseSubject.TOAN,
        VietnameseSubject.HOA_HOC,
    ],
    "C03": [
        VietnameseSubject.VAN,
        VietnameseSubject.TOAN,
        VietnameseSubject.SU,
    ],
    "C04": [
        VietnameseSubject.VAN,
        VietnameseSubject.TOAN,
        VietnameseSubject.DIA,
    ],
    "C05": [
        VietnameseSubject.VAN,
        VietnameseSubject.VAT_LY,
        VietnameseSubject.HOA_HOC,
    ],
    "C06": [
        VietnameseSubject.VAN,
        VietnameseSubject.VAT_LY,
        VietnameseSubject.SINH,
    ],
    "C07": [
        VietnameseSubject.VAN,
        VietnameseSubject.VAT_LY,
        VietnameseSubject.SU,
    ],
    "C08": [
        VietnameseSubject.VAN,
        VietnameseSubject.HOA_HOC,
        VietnameseSubject.SINH,
    ],
    "C09": [
        VietnameseSubject.VAN,
        VietnameseSubject.VAT_LY,
        VietnameseSubject.DIA,
    ],
    "C10": [
        VietnameseSubject.VAN,
        VietnameseSubject.HOA_HOC,
        VietnameseSubject.SU,
    ],
    "C12": [
        VietnameseSubject.VAN,
        VietnameseSubject.SINH,
        VietnameseSubject.SU,
    ],
    "C13": [
        VietnameseSubject.VAN,
        VietnameseSubject.SINH,
        VietnameseSubject.DIA,
    ],
    "C14": [
        VietnameseSubject.VAN,
        VietnameseSubject.TOAN,
        VietnameseSubject.GDKT_PL,
    ],
    "C15": [
        VietnameseSubject.VAN,
        VietnameseSubject.TOAN,
        VietnameseSubject.KHOA_HOC_XA_HOI,
    ],
    "C16": [
        VietnameseSubject.VAN,
        VietnameseSubject.VAT_LY,
        VietnameseSubject.GDKT_PL,
    ],
    "C17": [
        VietnameseSubject.VAN,
        VietnameseSubject.HOA_HOC,
        VietnameseSubject.GDKT_PL,
    ],
    "C18": [
        VietnameseSubject.VAN,
        VietnameseSubject.SINH,
        VietnameseSubject.GDKT_PL,
    ],
    "C19": [
        VietnameseSubject.VAN,
        VietnameseSubject.SU,
        VietnameseSubject.GDKT_PL,
    ],
    "C20": [
        VietnameseSubject.VAN,
        VietnameseSubject.DIA,
        VietnameseSubject.GDKT_PL,
    ],

    # Khối D
    "D01": [
        VietnameseSubject.VAN,
        VietnameseSubject.TOAN,
        VietnameseSubject.TIENG_ANH,
    ],
    "D02": [
        VietnameseSubject.VAN,
        VietnameseSubject.TOAN,
        VietnameseSubject.TIENG_NGA,
    ],
    "D03": [
        VietnameseSubject.VAN,
        VietnameseSubject.TOAN,
        VietnameseSubject.TIENG_PHAP,
    ],
    "D04": [
        VietnameseSubject.VAN,
        VietnameseSubject.TOAN,
        VietnameseSubject.TIENG_TRUNG,
    ],
    "D05": [
        VietnameseSubject.VAN,
        VietnameseSubject.TOAN,
        VietnameseSubject.TIENG_DUC,
    ],
    "D06": [
        VietnameseSubject.VAN,
        VietnameseSubject.TOAN,
        VietnameseSubject.TIENG_NHAT,
    ],
    "D07": [
        VietnameseSubject.TOAN,
        VietnameseSubject.HOA_HOC,
        VietnameseSubject.TIENG_ANH,
    ],
    "D08": [
        VietnameseSubject.TOAN,
        VietnameseSubject.SINH,
        VietnameseSubject.TIENG_ANH,
    ],
    "D09": [
        VietnameseSubject.TOAN,
        VietnameseSubject.SU,
        VietnameseSubject.TIENG_ANH,
    ],
    "D10": [
        VietnameseSubject.TOAN,
        VietnameseSubject.DIA,
        VietnameseSubject.TIENG_ANH,
    ],
    "D11": [
        VietnameseSubject.VAN,
        VietnameseSubject.VAT_LY,
        VietnameseSubject.TIENG_ANH,
    ],
    "D12": [
        VietnameseSubject.VAN,
        VietnameseSubject.HOA_HOC,
        VietnameseSubject.TIENG_ANH,
    ],
    "D13": [
        VietnameseSubject.VAN,
        VietnameseSubject.SINH,
        VietnameseSubject.TIENG_ANH,
    ],
    "D14": [
        VietnameseSubject.VAN,
        VietnameseSubject.SU,
        VietnameseSubject.TIENG_ANH,
    ],
    "D15": [
        VietnameseSubject.VAN,
        VietnameseSubject.DIA,
        VietnameseSubject.TIENG_ANH,
    ],
    "D16": [
        VietnameseSubject.VAN,
        VietnameseSubject.DIA,
        VietnameseSubject.TIENG_DUC,
    ],
    "D17": [
        VietnameseSubject.VAN,
        VietnameseSubject.DIA,
        VietnameseSubject.TIENG_NGA,
    ],
    "D18": [
        VietnameseSubject.VAN,
        VietnameseSubject.DIA,
        VietnameseSubject.TIENG_NHAT,
    ],
    "D19": [
        VietnameseSubject.VAN,
        VietnameseSubject.DIA,
        VietnameseSubject.TIENG_PHAP,
    ],
    "D20": [
        VietnameseSubject.TOAN,
        VietnameseSubject.DIA,
        VietnameseSubject.TIENG_TRUNG,
    ],
    "D21": [
        VietnameseSubject.TOAN,
        VietnameseSubject.HOA_HOC,
        VietnameseSubject.TIENG_DUC,
    ],
    "D22": [
        VietnameseSubject.TOAN,
        VietnameseSubject.HOA_HOC,
        VietnameseSubject.TIENG_NGA,
    ],
    "D23": [
        VietnameseSubject.TOAN,
        VietnameseSubject.HOA_HOC,
        VietnameseSubject.TIENG_NHAT,
    ],
    "D24": [
        VietnameseSubject.TOAN,
        VietnameseSubject.HOA_HOC,
        VietnameseSubject.TIENG_PHAP,
    ],
    "D25": [
        VietnameseSubject.TOAN,
        VietnameseSubject.HOA_HOC,
        VietnameseSubject.TIENG_TRUNG,
    ],
    "D26": [
        VietnameseSubject.TOAN,
        VietnameseSubject.VAT_LY,
        VietnameseSubject.TIENG_DUC,
    ],
    "D27": [
        VietnameseSubject.TOAN,
        VietnameseSubject.VAT_LY,
        VietnameseSubject.TIENG_NGA,
    ],
    "D28": [
        VietnameseSubject.TOAN,
        VietnameseSubject.VAT_LY,
        VietnameseSubject.TIENG_NHAT,
    ],
    "D29": [
        VietnameseSubject.TOAN,
        VietnameseSubject.VAT_LY,
        VietnameseSubject.TIENG_PHAP,
    ],
    "D30": [
        VietnameseSubject.TOAN,
        VietnameseSubject.VAT_LY,
        VietnameseSubject.TIENG_TRUNG,
    ],
    "D31": [
        VietnameseSubject.TOAN,
        VietnameseSubject.SINH,
        VietnameseSubject.TIENG_DUC,
    ],
    "D32": [
        VietnameseSubject.TOAN,
        VietnameseSubject.SINH,
        VietnameseSubject.TIENG_NGA,
    ],
    "D33": [
        VietnameseSubject.TOAN,
        VietnameseSubject.SINH,
        VietnameseSubject.TIENG_NHAT,
    ],
    "D34": [
        VietnameseSubject.TOAN,
        VietnameseSubject.SINH,
        VietnameseSubject.TIENG_PHAP,
    ],
    "D35": [
        VietnameseSubject.TOAN,
        VietnameseSubject.SINH,
        VietnameseSubject.TIENG_TRUNG,
    ],
    "D41": [
        VietnameseSubject.VAN,
        VietnameseSubject.DIA,
        VietnameseSubject.TIENG_DUC,
    ],
    "D42": [
        VietnameseSubject.VAN,
        VietnameseSubject.DIA,
        VietnameseSubject.TIENG_NGA,
    ],
    "D43": [
        VietnameseSubject.VAN,
        VietnameseSubject.DIA,
        VietnameseSubject.TIENG_NHAT,
    ],
    "D44": [
        VietnameseSubject.VAN,
        VietnameseSubject.DIA,
        VietnameseSubject.TIENG_PHAP,
    ],
    "D45": [
        VietnameseSubject.VAN,
        VietnameseSubject.DIA,
        VietnameseSubject.TIENG_TRUNG,
    ],
    "D51": [
        VietnameseSubject.VAN,
        VietnameseSubject.VAT_LY,
        VietnameseSubject.TIENG_DUC,
    ],
    "D52": [
        VietnameseSubject.VAN,
        VietnameseSubject.VAT_LY,
        VietnameseSubject.TIENG_NGA,
    ],
    "D53": [
        VietnameseSubject.VAN,
        VietnameseSubject.VAT_LY,
        VietnameseSubject.TIENG_NHAT,
    ],
    "D54": [
        VietnameseSubject.VAN,
        VietnameseSubject.VAT_LY,
        VietnameseSubject.TIENG_PHAP,
    ],
    "D55": [
        VietnameseSubject.VAN,
        VietnameseSubject.VAT_LY,
        VietnameseSubject.TIENG_TRUNG,
    ],
    "D56": [
        VietnameseSubject.VAN,
        VietnameseSubject.TOAN,
        VietnameseSubject.TIENG_DUC,
    ],
    "D57": [
        VietnameseSubject.VAN,
        VietnameseSubject.TOAN,
        VietnameseSubject.TIENG_NGA,
    ],
    "D58": [
        VietnameseSubject.VAN,
        VietnameseSubject.TOAN,
        VietnameseSubject.TIENG_NHAT,
    ],
    "D59": [
        VietnameseSubject.VAN,
        VietnameseSubject.TOAN,
        VietnameseSubject.TIENG_PHAP,
    ],
    "D60": [
        VietnameseSubject.VAN,
        VietnameseSubject.TOAN,
        VietnameseSubject.TIENG_TRUNG,
    ],
    "D61": [
        VietnameseSubject.VAN,
        VietnameseSubject.SU,
        VietnameseSubject.TIENG_DUC,
    ],
    "D62": [
        VietnameseSubject.VAN,
        VietnameseSubject.SU,
        VietnameseSubject.TIENG_NGA,
    ],
    "D63": [
        VietnameseSubject.VAN,
        VietnameseSubject.SU,
        VietnameseSubject.TIENG_NHAT,
    ],
    "D64": [
        VietnameseSubject.VAN,
        VietnameseSubject.SU,
        VietnameseSubject.TIENG_PHAP,
    ],
    "D65": [
        VietnameseSubject.VAN,
        VietnameseSubject.SU,
        VietnameseSubject.TIENG_TRUNG,
    ],
    "D66": [
        VietnameseSubject.VAN,
        VietnameseSubject.GDKT_PL,
        VietnameseSubject.TIENG_ANH,
    ],
    "D68": [
        VietnameseSubject.VAN,
        VietnameseSubject.GDKT_PL,
        VietnameseSubject.TIENG_NGA,
    ],
    "D70": [
        VietnameseSubject.VAN,
        VietnameseSubject.GDKT_PL,
        VietnameseSubject.TIENG_PHAP,
    ],
    "D71": [
        VietnameseSubject.VAN,
        VietnameseSubject.GDKT_PL,
        VietnameseSubject.TIENG_TRUNG,
    ],
    "D72": [
        VietnameseSubject.VAN,
        VietnameseSubject.KHOA_HOC_TU_NHIEN,
        VietnameseSubject.TIENG_ANH,
    ],
    "D73": [
        VietnameseSubject.VAN,
        VietnameseSubject.KHOA_HOC_TU_NHIEN,
        VietnameseSubject.TIENG_DUC,
    ],
    "D74": [
        VietnameseSubject.VAN,
        VietnameseSubject.KHOA_HOC_TU_NHIEN,
        VietnameseSubject.TIENG_NGA,
    ],
    "D75": [
        VietnameseSubject.VAN,
        VietnameseSubject.KHOA_HOC_TU_NHIEN,
        VietnameseSubject.TIENG_NHAT,
    ],
    "D76": [
        VietnameseSubject.VAN,
        VietnameseSubject.KHOA_HOC_TU_NHIEN,
        VietnameseSubject.TIENG_PHAP,
    ],
    "D77": [
        VietnameseSubject.VAN,
        VietnameseSubject.KHOA_HOC_TU_NHIEN,
        VietnameseSubject.TIENG_TRUNG,
    ],
    "D78": [
        VietnameseSubject.VAN,
        VietnameseSubject.KHOA_HOC_XA_HOI,
        VietnameseSubject.TIENG_ANH,
    ],
    "D79": [
        VietnameseSubject.VAN,
        VietnameseSubject.KHOA_HOC_XA_HOI,
        VietnameseSubject.TIENG_DUC,
    ],
    "D80": [
        VietnameseSubject.VAN,
        VietnameseSubject.KHOA_HOC_XA_HOI,
        VietnameseSubject.TIENG_NGA,
    ],
    "D81": [
        VietnameseSubject.VAN,
        VietnameseSubject.KHOA_HOC_XA_HOI,
        VietnameseSubject.TIENG_NHAT,
    ],
    "D82": [
        VietnameseSubject.VAN,
        VietnameseSubject.KHOA_HOC_XA_HOI,
        VietnameseSubject.TIENG_PHAP,
    ],
    "D83": [
        VietnameseSubject.VAN,
        VietnameseSubject.KHOA_HOC_XA_HOI,
        VietnameseSubject.TIENG_TRUNG,
    ],
    "D84": [
        VietnameseSubject.TOAN,
        VietnameseSubject.GDKT_PL,
        VietnameseSubject.TIENG_ANH,
    ],
    "D85": [
        VietnameseSubject.TOAN,
        VietnameseSubject.GDKT_PL,
        VietnameseSubject.TIENG_DUC,
    ],
    "D86": [
        VietnameseSubject.TOAN,
        VietnameseSubject.GDKT_PL,
        VietnameseSubject.TIENG_NGA,
    ],
    "D87": [
        VietnameseSubject.TOAN,
        VietnameseSubject.GDKT_PL,
        VietnameseSubject.TIENG_PHAP,
    ],
    "D88": [
        VietnameseSubject.TOAN,
        VietnameseSubject.GDKT_PL,
        VietnameseSubject.TIENG_NHAT,
    ],
    "D89": [
        VietnameseSubject.TOAN,
        VietnameseSubject.GDKT_PL,
        VietnameseSubject.TIENG_TRUNG,
    ],
    "D90": [
        VietnameseSubject.TOAN,
        VietnameseSubject.KHOA_HOC_TU_NHIEN,
        VietnameseSubject.TIENG_ANH,
    ],
    "D91": [
        VietnameseSubject.TOAN,
        VietnameseSubject.KHOA_HOC_TU_NHIEN,
        VietnameseSubject.TIENG_PHAP,
    ],
    "D92": [
        VietnameseSubject.TOAN,
        VietnameseSubject.KHOA_HOC_TU_NHIEN,
        VietnameseSubject.TIENG_DUC,
    ],
    "D93": [
        VietnameseSubject.TOAN,
        VietnameseSubject.KHOA_HOC_TU_NHIEN,
        VietnameseSubject.TIENG_NGA,
    ],
    "D94": [
        VietnameseSubject.TOAN,
        VietnameseSubject.KHOA_HOC_TU_NHIEN,
        VietnameseSubject.TIENG_NHAT,
    ],
    "D95": [
        VietnameseSubject.TOAN,
        VietnameseSubject.KHOA_HOC_TU_NHIEN,
        VietnameseSubject.TIENG_TRUNG,
    ],
    "D96": [
        VietnameseSubject.TOAN,
        VietnameseSubject.KHOA_HOC_XA_HOI,
        VietnameseSubject.TIENG_ANH,
    ],
    "D97": [
        VietnameseSubject.TOAN,
        VietnameseSubject.KHOA_HOC_XA_HOI,
        VietnameseSubject.TIENG_PHAP,
    ],
    "D98": [
        VietnameseSubject.TOAN,
        VietnameseSubject.KHOA_HOC_XA_HOI,
        VietnameseSubject.TIENG_DUC,
    ],
    "D99": [
        VietnameseSubject.TOAN,
        VietnameseSubject.KHOA_HOC_XA_HOI,
        VietnameseSubject.TIENG_NGA,
    ],
    "DD0": [
        VietnameseSubject.TOAN,
        VietnameseSubject.KHOA_HOC_XA_HOI,
        VietnameseSubject.TIENG_NHAT,
    ],
    "DD1": [
        VietnameseSubject.TOAN,
        VietnameseSubject.KHOA_HOC_XA_HOI,
        VietnameseSubject.TIENG_TRUNG,
    ],
    "DD2": [
        VietnameseSubject.VAN,
        VietnameseSubject.TOAN,
        VietnameseSubject.TIENG_HAN,
    ],

    # Khối H
    "H00": [
        VietnameseSubject.TOAN,
        VietnameseSubject.NANG_KHIEU_VE_1,
        VietnameseSubject.NANG_KHIEU_VE_2,
    ],
    "H01": [
        VietnameseSubject.TOAN,
        VietnameseSubject.VAN,
        VietnameseSubject.VE_MY_THUAT,
    ],
    "H02": [
        VietnameseSubject.TOAN,
        VietnameseSubject.VE_HINH_HOA_MY_THUAT,
        VietnameseSubject.VE_TRANG_TRI_MAU,
    ],
    "H03": [
        VietnameseSubject.TOAN,
        VietnameseSubject.KHOA_HOC_TU_NHIEN,
        VietnameseSubject.VE_TRANG_TRI_MAU,
    ],
    "H04": [
        VietnameseSubject.TOAN,
        VietnameseSubject.TIENG_ANH,
        VietnameseSubject.VE_NANG_KHIEU,
    ],
    "H05": [
        VietnameseSubject.VAN,
        VietnameseSubject.KHOA_HOC_XA_HOI,
        VietnameseSubject.VE_NANG_KHIEU,
    ],
    "H06": [
        VietnameseSubject.VAN,
        VietnameseSubject.TIENG_ANH,
        VietnameseSubject.VE_MY_THUAT,
    ],
    "H07": [
        VietnameseSubject.TOAN,
        VietnameseSubject.VE_HINH_HOA,
        VietnameseSubject.VE_TRANG_TRI,
    ],
    "H08": [
        VietnameseSubject.VAN,
        VietnameseSubject.SU,
        VietnameseSubject.VE_MY_THUAT,
    ],

    # Khối khác
    "K00": [
        VietnameseSubject.TOAN,
        VietnameseSubject.DOC_HIEU,
        VietnameseSubject.TU_DUY_GIAI_QUYET_NGU_VAN_DE,
    ],

    # Khối M
    "M00": [
        VietnameseSubject.VAN,
        VietnameseSubject.TOAN,
        VietnameseSubject.DOC_DIEN_CAM,
        VietnameseSubject.HAT,
    ],
    "M01": [
        VietnameseSubject.VAN,
        VietnameseSubject.SU,
        VietnameseSubject.NANG_KHIEU,
    ],
    "M02": [
        VietnameseSubject.TOAN,
        VietnameseSubject.NANG_KHIEU_1,
        VietnameseSubject.NANG_KHIEU_2,
    ],
    "M03": [
        VietnameseSubject.VAN,
        VietnameseSubject.NANG_KHIEU_1,
        VietnameseSubject.NANG_KHIEU_2,
    ],
    "M04": [
        VietnameseSubject.TOAN,
        VietnameseSubject.DOC_DIEN_CAM,
        VietnameseSubject.HAT_MUA,
    ],
    "M05": [
        VietnameseSubject.VAN,
        VietnameseSubject.SU,
        VietnameseSubject.NANG_KHIEU,
    ],
    "M06": [
        VietnameseSubject.VAN,
        VietnameseSubject.TOAN,
        VietnameseSubject.NANG_KHIEU,
    ],
    "M07": [
        VietnameseSubject.VAN,
        VietnameseSubject.DIA,
        VietnameseSubject.NANG_KHIEU,
    ],
    "M08": [
        VietnameseSubject.VAN,
        VietnameseSubject.NANG_KHIEU_1,
        VietnameseSubject.NANG_KHIEU_2,
    ],
    "M09": [
        VietnameseSubject.TOAN,
        VietnameseSubject.NANG_KHIEU_MAM_NON_1,
        VietnameseSubject.NANG_KHIEU_MAM_NON_2,
    ],
    "M10": [
        VietnameseSubject.TOAN,
        VietnameseSubject.TIENG_ANH,
        VietnameseSubject.NANG_KHIEU_MAM_NON,
    ],
    "M11": [
        VietnameseSubject.VAN,
        VietnameseSubject.TIENG_ANH,
        VietnameseSubject.NANG_KHIEU_MAM_NON,
    ],
    "M13": [
        VietnameseSubject.TOAN,
        VietnameseSubject.SINH,
        VietnameseSubject.NANG_KHIEU_MAM_NON,
    ],
    "M14": [
        VietnameseSubject.VAN,
        VietnameseSubject.DIA,
        VietnameseSubject.NANG_KHIEU_MAM_NON,
    ],

    # Khối N
    "N00": [
        VietnameseSubject.VAN,
        VietnameseSubject.NANG_KHIEU_AM_NHAC_1,
        VietnameseSubject.NANG_KHIEU_AM_NHAC_2,
    ],
    "N01": [
        VietnameseSubject.VAN,
        VietnameseSubject.HAT_XUONG_AM,
        VietnameseSubject.BIEU_DIEN_NGHE_THUAT,
    ],
    "N02": [
        VietnameseSubject.VAN,
        VietnameseSubject.KY_XUONG_AM,
        VietnameseSubject.HAT_BIEU_DIEN_NHAC_CU,
    ],
    "N03": [
        VietnameseSubject.VAN,
        VietnameseSubject.GHI_AM_XUONG_AM,
        VietnameseSubject.CHUYEN_MON_AM_NHAC,
    ],
    "N04": [
        VietnameseSubject.VAN,
        VietnameseSubject.NANG_KHIEU_THUYET_TRINH,
        VietnameseSubject.NANG_KHIEU,
    ],
    "N05": [
        VietnameseSubject.VAN,
        VietnameseSubject.XAY_DUNG_KICH_BAN_SU_KIEN,
        VietnameseSubject.NANG_KHIEU,
    ],
    "N06": [
        VietnameseSubject.VAN,
        VietnameseSubject.GHI_AM_XUONG_AM,
        VietnameseSubject.CHUYEN_MON_AM_NHAC_1,
    ],
    "N07": [
        VietnameseSubject.VAN,
        VietnameseSubject.GHI_AM_XUONG_AM,
        VietnameseSubject.CHUYEN_MON_AM_NHAC_2,
    ],
    "N08": [
        VietnameseSubject.VAN,
        VietnameseSubject.HOA_THANH,
        VietnameseSubject.PHAT_TRIEN_CHU_DE_PHO_THO,
    ],
    "N09": [
        VietnameseSubject.VAN,
        VietnameseSubject.HOA_THANH,
        VietnameseSubject.CHI_HUY_TAI_CHO,
    ],

    # Khối R
    "R00": [
        VietnameseSubject.VAN,
        VietnameseSubject.SU,
        VietnameseSubject.NANG_KHIEU_BAO_CHI,
    ],
    "R01": [
        VietnameseSubject.VAN,
        VietnameseSubject.DIA,
        VietnameseSubject.NANG_KHIEU_BIEU_DIEN_NGHE_THUAT,
    ],
    "R02": [
        VietnameseSubject.TOAN,
        VietnameseSubject.VAN,
        VietnameseSubject.NANG_KHIEU_BIEU_DIEN_NGHE_THUAT,
    ],
    "R03": [
        VietnameseSubject.VAN,
        VietnameseSubject.TIENG_ANH,
        VietnameseSubject.NANG_KHIEU_BIEU_DIEN_NGHE_THUAT,
    ],
    "R04": [
        VietnameseSubject.VAN,
        VietnameseSubject.NANG_KHIEU_BIEU_DIEN_NGHE_THUAT,
        VietnameseSubject.NANG_KHIEU_KIEN_THUC_VAN_HOA_XA_HOI_NGHE_THUAT,
    ],
    "R05": [
        VietnameseSubject.VAN,
        VietnameseSubject.TIENG_ANH,
        VietnameseSubject.NANG_KHIEU_BAO_CHI,
    ],
    "R06": [
        VietnameseSubject.VAN,
        VietnameseSubject.KHOA_HOC_TU_NHIEN,
        VietnameseSubject.NANG_KHIEU_BAO_CHI,
    ],
    "R07": [
        VietnameseSubject.TOAN,
        VietnameseSubject.VAN,
        VietnameseSubject.NANG_KHIEU_ANH_BAO_CHI,
    ],
    "R08": [
        VietnameseSubject.VAN,
        VietnameseSubject.TIENG_ANH,
        VietnameseSubject.NANG_KHIEU_ANH_BAO_CHI,
    ],
    "R09": [
        VietnameseSubject.VAN,
        VietnameseSubject.KHOA_HOC_TU_NHIEN,
        VietnameseSubject.NANG_KHIEU_ANH_BAO_CHI,
    ],
    "R11": [
        VietnameseSubject.TOAN,
        VietnameseSubject.VAN,
        VietnameseSubject.NANG_KHIEU_QUAY_PHIM_TRUYEN_HINH,
    ],
    "R12": [
        VietnameseSubject.VAN,
        VietnameseSubject.TIENG_ANH,
        VietnameseSubject.NANG_KHIEU_QUAY_PHIM_TRUYEN_HINH,
    ],
    "R13": [
        VietnameseSubject.VAN,
        VietnameseSubject.KHOA_HOC_TU_NHIEN,
        VietnameseSubject.NANG_KHIEU_QUAY_PHIM_TRUYEN_HINH,
    ],
    "R15": [
        VietnameseSubject.TOAN,
        VietnameseSubject.VAN,
        VietnameseSubject.NANG_KHIEU_BAO_CHI,
    ],
    "R16": [
        VietnameseSubject.VAN,
        VietnameseSubject.KHOA_HOC_XA_HOI,
        VietnameseSubject.NANG_KHIEU_BAO_CHI,
    ],
    "R17": [
        VietnameseSubject.VAN,
        VietnameseSubject.KHOA_HOC_XA_HOI,
        VietnameseSubject.NANG_KHIEU_ANH_BAO_CHI,
    ],
    "R18": [
        VietnameseSubject.VAN,
        VietnameseSubject.KHOA_HOC_XA_HOI,
        VietnameseSubject.NANG_KHIEU_QUAY_PHIM_TRUYEN_HINH,
    ],
    "R19": [
        VietnameseSubject.VAN,
        VietnameseSubject.CHUNG_CHI_QUY_DOI_TIENG_ANH,
        VietnameseSubject.NANG_KHIEU_BAO_CHI,
    ],
    "R20": [
        VietnameseSubject.VAN,
        VietnameseSubject.CHUNG_CHI_QUY_DOI_TIENG_ANH,
        VietnameseSubject.NANG_KHIEU_ANH_BAO_CHI,
    ],
    "R21": [
        VietnameseSubject.VAN,
        VietnameseSubject.CHUNG_CHI_QUY_DOI_TIENG_ANH,
        VietnameseSubject.NANG_KHIEU_QUAY_PHIM_TRUYEN_HINH,
    ],
    "R22": [
        VietnameseSubject.TOAN,
        VietnameseSubject.VAN,
        VietnameseSubject.CHUNG_CHI_QUY_DOI_TIENG_ANH,
    ],
    "R23": [
        VietnameseSubject.VAN,
        VietnameseSubject.SU,
        VietnameseSubject.CHUNG_CHI_QUY_DOI_TIENG_ANH,
    ],
    "R24": [
        VietnameseSubject.TOAN,
        VietnameseSubject.VAN,
        VietnameseSubject.CHUNG_CHI_QUY_DOI_TIENG_ANH,
    ],
    "R25": [
        VietnameseSubject.VAN,
        VietnameseSubject.KHOA_HOC_TU_NHIEN,
        VietnameseSubject.CHUNG_CHI_QUY_DOI_TIENG_ANH,
    ],
    "R26": [
        VietnameseSubject.VAN,
        VietnameseSubject.KHOA_HOC_XA_HOI,
        VietnameseSubject.CHUNG_CHI_QUY_DOI_TIENG_ANH,
    ],

    # Khối S
    "S00": [
        VietnameseSubject.VAN,
        VietnameseSubject.NANG_KHIEU_SKDA_1,
        VietnameseSubject.NANG_KHIEU_SKDA_2,
    ],
    "S01": [
        VietnameseSubject.TOAN,
        VietnameseSubject.NANG_KHIEU_SKDA_1,
        VietnameseSubject.NANG_KHIEU_SKDA_2,
    ],

    # Khối T
    "T00": [
        VietnameseSubject.TOAN,
        VietnameseSubject.SINH,
        VietnameseSubject.NANG_KHIEU_TDTT,
    ],
    "T01": [
        VietnameseSubject.TOAN,
        VietnameseSubject.VAN,
        VietnameseSubject.NANG_KHIEU_TDTT,
    ],
    "T02": [
        VietnameseSubject.VAN,
        VietnameseSubject.SINH,
        VietnameseSubject.NANG_KHIEU_TDTT,
    ],
    "T03": [
        VietnameseSubject.VAN,
        VietnameseSubject.DIA,
        VietnameseSubject.NANG_KHIEU_TDTT,
    ],
    "T04": [
        VietnameseSubject.TOAN,
        VietnameseSubject.VAT_LY,
        VietnameseSubject.NANG_KHIEU_TDTT,
    ],
    "T05": [
        VietnameseSubject.VAN,
        VietnameseSubject.GDKT_PL,
        VietnameseSubject.NANG_KHIEU_TDTT,
    ],
    "T06": [
        VietnameseSubject.TOAN,
        VietnameseSubject.DIA,
        VietnameseSubject.NANG_KHIEU_TDTT,
    ],
    "T07": [
        VietnameseSubject.VAN,
        VietnameseSubject.DIA,
        VietnameseSubject.NANG_KHIEU_TDTT,
    ],
    "T08": [
        VietnameseSubject.TOAN,
        VietnameseSubject.GDKT_PL,
        VietnameseSubject.NANG_KHIEU_TDTT,
    ],
    "T10": [
        VietnameseSubject.TOAN,
        VietnameseSubject.TIENG_ANH,
        VietnameseSubject.NANG_KHIEU_TDTT,
    ],

    # Khối V
    "V00": [
        VietnameseSubject.TOAN,
        VietnameseSubject.VAT_LY,
        VietnameseSubject.VE_MY_THUAT,
    ],
    "V01": [
        VietnameseSubject.TOAN,
        VietnameseSubject.VAN,
        VietnameseSubject.VE_MY_THUAT,
    ],
    "V02": [
        VietnameseSubject.TOAN,
        VietnameseSubject.TIENG_ANH,
        VietnameseSubject.VE_MY_THUAT,
    ],
    "V03": [
        VietnameseSubject.TOAN,
        VietnameseSubject.HOA_HOC,
        VietnameseSubject.VE_MY_THUAT,
    ],
    "V05": [
        VietnameseSubject.VAN,
        VietnameseSubject.VAT_LY,
        VietnameseSubject.VE_MY_THUAT,
    ],
    "V06": [
        VietnameseSubject.TOAN,
        VietnameseSubject.DIA,
        VietnameseSubject.VE_MY_THUAT,
    ],
    "V07": [
        VietnameseSubject.TOAN,
        VietnameseSubject.TIENG_DUC,
        VietnameseSubject.VE_MY_THUAT,
    ],
    "V08": [
        VietnameseSubject.TOAN,
        VietnameseSubject.TIENG_NGA,
        VietnameseSubject.VE_MY_THUAT,
    ],
    "V09": [
        VietnameseSubject.TOAN,
        VietnameseSubject.TIENG_NHAT,
        VietnameseSubject.VE_MY_THUAT,
    ],
    "V10": [
        VietnameseSubject.TOAN,
        VietnameseSubject.TIENG_PHAP,
        VietnameseSubject.VE_MY_THUAT,
    ],
    "V11": [
        VietnameseSubject.TOAN,
        VietnameseSubject.TIENG_TRUNG,
        VietnameseSubject.VE_MY_THUAT,
    ],

    "X01": [
        VietnameseSubject.TOAN,
        VietnameseSubject.VAN,
        VietnameseSubject.GDKT_PL,
    ],
    "X02": [
        VietnameseSubject.TOAN,
        VietnameseSubject.VAN,
        VietnameseSubject.TIN,
    ],
    "X03": [
        VietnameseSubject.TOAN,
        VietnameseSubject.VAN,
        VietnameseSubject.CONG_NGHE_CONG_NGHIEP,
    ],
    "X04": [
        VietnameseSubject.TOAN,
        VietnameseSubject.VAN,
        VietnameseSubject.CONG_NGHE_NONG_NGHIEP,
    ],
    "X05": [
        VietnameseSubject.TOAN,
        VietnameseSubject.VAT_LY,
        VietnameseSubject.GDKT_PL,
    ],
    "X06": [
        VietnameseSubject.TOAN,
        VietnameseSubject.VAT_LY,
        VietnameseSubject.TIN,
    ],
    "X07": [
        VietnameseSubject.TOAN,
        VietnameseSubject.VAT_LY,
        VietnameseSubject.CONG_NGHE_CONG_NGHIEP,
    ],
    "X08": [
        VietnameseSubject.TOAN,
        VietnameseSubject.VAT_LY,
        VietnameseSubject.CONG_NGHE_NONG_NGHIEP,
    ],
    "X09": [
        VietnameseSubject.TOAN,
        VietnameseSubject.HOA_HOC,
        VietnameseSubject.GDKT_PL,
    ],
    "X10": [
        VietnameseSubject.TOAN,
        VietnameseSubject.HOA_HOC,
        VietnameseSubject.TIN,
    ],
    "X11": [
        VietnameseSubject.TOAN,
        VietnameseSubject.HOA_HOC,
        VietnameseSubject.CONG_NGHE_CONG_NGHIEP,
    ],
    "X12": [
        VietnameseSubject.TOAN,
        VietnameseSubject.HOA_HOC,
        VietnameseSubject.CONG_NGHE_NONG_NGHIEP,
    ],
    "X13": [
        VietnameseSubject.TOAN,
        VietnameseSubject.SINH,
        VietnameseSubject.GDKT_PL,
    ],
    "X14": [
        VietnameseSubject.TOAN,
        VietnameseSubject.SINH,
        VietnameseSubject.TIN,
    ],
    "X15": [
        VietnameseSubject.TOAN,
        VietnameseSubject.SINH,
        VietnameseSubject.CONG_NGHE_CONG_NGHIEP,
    ],
    "X16": [
        VietnameseSubject.TOAN,
        VietnameseSubject.SINH,
        VietnameseSubject.CONG_NGHE_NONG_NGHIEP,
    ],
    "X17": [
        VietnameseSubject.TOAN,
        VietnameseSubject.SU,
        VietnameseSubject.GDKT_PL,
    ],
    "X18": [
        VietnameseSubject.TOAN,
        VietnameseSubject.SU,
        VietnameseSubject.TIN,
    ],
    "X19": [
        VietnameseSubject.TOAN,
        VietnameseSubject.SU,
        VietnameseSubject.CONG_NGHE_CONG_NGHIEP,
    ],
    "X20": [
        VietnameseSubject.TOAN,
        VietnameseSubject.SU,
        VietnameseSubject.CONG_NGHE_NONG_NGHIEP,
    ],
    "X21": [
        VietnameseSubject.TOAN,
        VietnameseSubject.DIA,
        VietnameseSubject.GDKT_PL,
    ],
    "X22": [
        VietnameseSubject.TOAN,
        VietnameseSubject.DIA,
        VietnameseSubject.TIN,
    ],
    "X23": [
        VietnameseSubject.TOAN,
        VietnameseSubject.DIA,
        VietnameseSubject.CONG_NGHE_CONG_NGHIEP,
    ],
    "X24": [
        VietnameseSubject.TOAN,
        VietnameseSubject.DIA,
        VietnameseSubject.CONG_NGHE_NONG_NGHIEP,
    ],
    "X25": [
        VietnameseSubject.TOAN,
        VietnameseSubject.TIENG_ANH,
        VietnameseSubject.GDKT_PL,
    ],
    "X26": [
        VietnameseSubject.TOAN,
        VietnameseSubject.TIENG_ANH,
        VietnameseSubject.TIN,
    ],
    "X27": [
        VietnameseSubject.TOAN,
        VietnameseSubject.TIENG_ANH,
        VietnameseSubject.CONG_NGHE_CONG_NGHIEP,
    ],
    "X28": [
        VietnameseSubject.TOAN,
        VietnameseSubject.TIENG_ANH,
        VietnameseSubject.CONG_NGHE_NONG_NGHIEP,
    ],
    "X29": [
        VietnameseSubject.TOAN,
        VietnameseSubject.GDKT_PL,
        VietnameseSubject.TIENG_NGA,
    ],
    "X33": [
        VietnameseSubject.TOAN,
        VietnameseSubject.GDKT_PL,
        VietnameseSubject.TIENG_PHAP,
    ],
    "X45": [
        VietnameseSubject.TOAN,
        VietnameseSubject.GDKT_PL,
        VietnameseSubject.TIENG_NHAT,
    ],
    "X46": [
        VietnameseSubject.TOAN,
        VietnameseSubject.TIN,
        VietnameseSubject.TIENG_NHAT,
    ],
    "X53": [
        VietnameseSubject.TOAN,
        VietnameseSubject.GDKT_PL,
        VietnameseSubject.TIN,
    ],
    "X54": [
        VietnameseSubject.TOAN,
        VietnameseSubject.GDKT_PL,
        VietnameseSubject.CONG_NGHE_CONG_NGHIEP,
    ],
    "X55": [
        VietnameseSubject.TOAN,
        VietnameseSubject.GDKT_PL,
        VietnameseSubject.CONG_NGHE_NONG_NGHIEP,
    ],
    "X56": [
        VietnameseSubject.TOAN,
        VietnameseSubject.TIN,
        VietnameseSubject.CONG_NGHE_CONG_NGHIEP,
    ],
    "X57": [
        VietnameseSubject.TOAN,
        VietnameseSubject.TIN,
        VietnameseSubject.CONG_NGHE_CONG_NGHIEP,
    ],
    "X58": [
        VietnameseSubject.VAN,
        VietnameseSubject.VAT_LY,
        VietnameseSubject.GDKT_PL,
    ],
    "X59": [
        VietnameseSubject.VAN,
        VietnameseSubject.VAT_LY,
        VietnameseSubject.TIN,
    ],
    "X60": [
        VietnameseSubject.VAN,
        VietnameseSubject.VAT_LY,
        VietnameseSubject.CONG_NGHE_CONG_NGHIEP,
    ],
    "X61": [
        VietnameseSubject.VAN,
        VietnameseSubject.VAT_LY,
        VietnameseSubject.CONG_NGHE_NONG_NGHIEP,
    ],
    "X62": [
        VietnameseSubject.VAN,
        VietnameseSubject.HOA_HOC,
        VietnameseSubject.GDKT_PL,
    ],
    "X63": [
        VietnameseSubject.VAN,
        VietnameseSubject.HOA_HOC,
        VietnameseSubject.TIN,
    ],
    "X64": [
        VietnameseSubject.VAN,
        VietnameseSubject.HOA_HOC,
        VietnameseSubject.CONG_NGHE_CONG_NGHIEP,
    ],
    "X65": [
        VietnameseSubject.VAN,
        VietnameseSubject.HOA_HOC,
        VietnameseSubject.CONG_NGHE_NONG_NGHIEP,
    ],
    "X66": [
        VietnameseSubject.VAN,
        VietnameseSubject.SINH,
        VietnameseSubject.GDKT_PL,
    ],
    "X67": [
        VietnameseSubject.VAN,
        VietnameseSubject.SINH,
        VietnameseSubject.TIN,
    ],
    "X68": [
        VietnameseSubject.VAN,
        VietnameseSubject.SINH,
        VietnameseSubject.CONG_NGHE_CONG_NGHIEP,
    ],
    "X69": [
        VietnameseSubject.VAN,
        VietnameseSubject.SINH,
        VietnameseSubject.CONG_NGHE_NONG_NGHIEP,
    ],
    "X70": [
        VietnameseSubject.VAN,
        VietnameseSubject.SU,
        VietnameseSubject.GDKT_PL,
    ],
    "X71": [
        VietnameseSubject.VAN,
        VietnameseSubject.SU,
        VietnameseSubject.TIN,
    ],
    "X72": [
        VietnameseSubject.VAN,
        VietnameseSubject.SU,
        VietnameseSubject.CONG_NGHE_CONG_NGHIEP,
    ],
    "X73": [
        VietnameseSubject.VAN,
        VietnameseSubject.SU,
        VietnameseSubject.CONG_NGHE_NONG_NGHIEP,
    ],
    "X74": [
        VietnameseSubject.VAN,
        VietnameseSubject.DIA,
        VietnameseSubject.GDKT_PL,
    ],
    "X75": [
        VietnameseSubject.VAN,
        VietnameseSubject.DIA,
        VietnameseSubject.TIN,
    ],
    "X76": [
        VietnameseSubject.VAN,
        VietnameseSubject.DIA,
        VietnameseSubject.CONG_NGHE_CONG_NGHIEP,
    ],
    "X77": [
        VietnameseSubject.VAN,
        VietnameseSubject.DIA,
        VietnameseSubject.CONG_NGHE_NONG_NGHIEP,
    ],
    "X78": [
        VietnameseSubject.VAN,
        VietnameseSubject.GDKT_PL,
        VietnameseSubject.TIENG_ANH,
    ],
    "X79": [
        VietnameseSubject.VAN,
        VietnameseSubject.TIENG_ANH,
        VietnameseSubject.TIN,
    ],
    "X80": [
        VietnameseSubject.VAN,
        VietnameseSubject.TIENG_ANH,
        VietnameseSubject.CONG_NGHE_CONG_NGHIEP,
    ],
    "X81": [
        VietnameseSubject.VAN,
        VietnameseSubject.TIENG_ANH,
        VietnameseSubject.CONG_NGHE_NONG_NGHIEP,
    ],
    "X86": [
        VietnameseSubject.VAN,
        VietnameseSubject.GDKT_PL,
        VietnameseSubject.TIENG_PHAP,
    ],
    "X90": [
        VietnameseSubject.VAN,
        VietnameseSubject.GDKT_PL,
        VietnameseSubject.TIENG_TRUNG,
    ],
    "X91": [
        VietnameseSubject.VAN,
        VietnameseSubject.TIN,
        VietnameseSubject.TIENG_TRUNG,
    ],
    "X98": [
        VietnameseSubject.VAN,
        VietnameseSubject.GDKT_PL,
        VietnameseSubject.TIENG_NHAT,
    ],
    "Y07": [
        VietnameseSubject.VAN,
        VietnameseSubject.GDKT_PL,
        VietnameseSubject.TIN,
    ],
    "Y08": [
        VietnameseSubject.VAN,
        VietnameseSubject.GDKT_PL,
        VietnameseSubject.CONG_NGHE_CONG_NGHIEP,
    ],
    "Y09": [
        VietnameseSubject.VAN,
        VietnameseSubject.GDKT_PL,
        VietnameseSubject.CONG_NGHE_NONG_NGHIEP,
    ],
    "TAC": [
        VietnameseSubject.TOAN,
        VietnameseSubject.TIENG_ANH,
        VietnameseSubject.CONG_NGHE_CONG_NGHIEP,
    ],
    "TAT": [
        VietnameseSubject.TOAN,
        VietnameseSubject.TIENG_ANH,
        VietnameseSubject.TIN,
    ],
    "THC": [
        VietnameseSubject.TOAN,
        VietnameseSubject.HOA_HOC,
        VietnameseSubject.CONG_NGHE_CONG_NGHIEP,
    ],
    "TLC": [
        VietnameseSubject.TOAN,
        VietnameseSubject.VAT_LY,
        VietnameseSubject.CONG_NGHE_CONG_NGHIEP,
    ],
    "TLT": [
        VietnameseSubject.TOAN,
        VietnameseSubject.VAT_LY,
        VietnameseSubject.TIN,
    ],
    "TSC": [
        VietnameseSubject.TOAN,
        VietnameseSubject.SINH,
        VietnameseSubject.CONG_NGHE_CONG_NGHIEP,
    ],
    "TVC": [
        VietnameseSubject.TOAN,
        VietnameseSubject.VAN,
        VietnameseSubject.CONG_NGHE_CONG_NGHIEP,
    ],
    "TVL": [
        VietnameseSubject.VAN,
        VietnameseSubject.VAT_LY,
        VietnameseSubject.TIN,
    ],
    "TVS": [
        VietnameseSubject.VAN,
        VietnameseSubject.SINH,
        VietnameseSubject.TIN,
    ],
    "TVT": [
        VietnameseSubject.TOAN,
        VietnameseSubject.VAN,
        VietnameseSubject.TIN,
    ],
    "VAT": [
        VietnameseSubject.VAN,
        VietnameseSubject.TIENG_ANH,
        VietnameseSubject.TIN,
    ],
    "VSC": [
        VietnameseSubject.VAN,
        VietnameseSubject.SINH,
        VietnameseSubject.CONG_NGHE_CONG_NGHIEP,
    ],
})

class OtherSbujectHandle(StrEnum):
    TOEFLiBT = "TOEFLiBT"
    TOEIC = "TOEIC"
    IELTS = "IELTS"
    HSA = "HSA"
    TSA = "TSA"
    SAT = "SAT"
    ACT = "ACT"
    IB = "IB"
    OSSD = "OSSD"
    Alevel = "Alevel"
    DoulingoEnglishTest = "DoulingoEnglishTest"
    PTEAcademic = "PTEAcademic"
    TestAS_Kinhtế = "TestAS(Kinhtế)"
    TestAS_Toánhọc_KHMT_KHTN = "TestAS(Toánhọc,KHMT,KHTN)"
    TestAS_Kỹthuật = "TestAS(Kỹthuật)"
    H = "H"
    TOEFLIPT = "TOEFLIPT"
    THT = "THT"
    TLT = "TLT"
    TST = "TST"
    TTA = "TTA"
    TVK = "TVK"
    VNUHCM = "VNUHCM"


class TinhTP(StrEnum):
    AN_GIANG = "An Giang"
    BAC_LIEU = "Bạc Liêu"
    BINH_DUONG = "Bình Dương"
    BINH_PHUOC = "Bình Phước"
    CA_MAU = "Cà Mau"
    CAN_THO = "Cần Thơ"
    DONG_NAI = "Đồng Nai"
    DONG_THAP = "Đồng Tháp"
    DA_LAT = "Đà Lạt"
    HAU_GIANG = "Hậu Giang"
    HO_CHI_MINH = "TP. Hồ Chí Minh"
    KIEN_GIANG = "Kiên Giang"
    LONG_AN = "Long An"
    TIEN_GIANG = "Tiền Giang"
    TRA_VINH = "Trà Vinh"
    VINH_LONG = "Vĩnh Long"
    VUNG_TAU = "Vũng Tàu"

HSG_SUBJECTS = [
    VietnameseSubject.SINH,
    VietnameseSubject.HOA_HOC,
    VietnameseSubject.TIENG_TRUNG,
    VietnameseSubject.TIENG_ANH,
    VietnameseSubject.TIENG_PHAP,
    VietnameseSubject.DIA,
    VietnameseSubject.SU,
    VietnameseSubject.TIN,
    VietnameseSubject.TIENG_NHAT,
    VietnameseSubject.VAN,
    VietnameseSubject.TOAN,
    VietnameseSubject.VAT_LY,
    VietnameseSubject.TIENG_NGA
]

SubjectGroup = Enum("SubjectGroup", {key: key for key in SUBJECT_GROUPS})
L2SubjectGroup = Enum(
    "L2SubjectGroup",
    {key: key for key in SUBJECT_GROUPS} |
    {key: key.value for key in OtherSbujectHandle}
)

HSGSubject = Enum("HSGSubject", {item.name: item.value for item in HSG_SUBJECTS})

SUBJECTNAME_MAIN = [
    VietnameseSubject.TOAN,
    VietnameseSubject.VAN,
    VietnameseSubject.TIENG_ANH,
    VietnameseSubject.TIENG_DUC,
    VietnameseSubject.TIENG_HAN,
    VietnameseSubject.TIENG_NGA,
    VietnameseSubject.TIENG_NHAT,
    VietnameseSubject.TIENG_PHAP,
    VietnameseSubject.TIENG_TRUNG,
    VietnameseSubject.VAT_LY,
    VietnameseSubject.HOA_HOC,
    VietnameseSubject.SINH,
    VietnameseSubject.SU,
    VietnameseSubject.DIA,
    VietnameseSubject.GDKT_PL,
    VietnameseSubject.TIN,
    VietnameseSubject.CONG_NGHE_CONG_NGHIEP,
    VietnameseSubject.CONG_NGHE_NONG_NGHIEP
]

SubjectName = Enum("SubjectName", {item.name: item.value for item in SUBJECTNAME_MAIN})

NANG_KHIEU = [
    VietnameseSubject.BIEU_DIEN_NGHE_THUAT,
    VietnameseSubject.CHI_HUY_TAI_CHO,
    VietnameseSubject.CHUYEN_MON_AM_NHAC,
    VietnameseSubject.CHUYEN_MON_AM_NHAC_1,
    VietnameseSubject.CHUYEN_MON_AM_NHAC_2,
    VietnameseSubject.DOC_DIEN_CAM,
    VietnameseSubject.DOC_HIEU,
    VietnameseSubject.GHI_AM_XUONG_AM,
    VietnameseSubject.HAT,
    VietnameseSubject.HAT_BIEU_DIEN_NHAC_CU,
    VietnameseSubject.HAT_MUA,
    VietnameseSubject.HAT_XUONG_AM,
    VietnameseSubject.HOA_THANH,
    VietnameseSubject.KY_XUONG_AM,
    VietnameseSubject.NANG_KHIEU,
    VietnameseSubject.NANG_KHIEU_1,
    VietnameseSubject.NANG_KHIEU_2,
    VietnameseSubject.NANG_KHIEU_AM_NHAC_1,
    VietnameseSubject.NANG_KHIEU_AM_NHAC_2,
    VietnameseSubject.NANG_KHIEU_ANH_BAO_CHI,
    VietnameseSubject.NANG_KHIEU_BAO_CHI,
    VietnameseSubject.NANG_KHIEU_BIEU_DIEN_NGHE_THUAT,
    VietnameseSubject.NANG_KHIEU_KIEN_THUC_VAN_HOA_XA_HOI_NGHE_THUAT,
    VietnameseSubject.NANG_KHIEU_MAM_NON,
    VietnameseSubject.NANG_KHIEU_MAM_NON_1,
    VietnameseSubject.NANG_KHIEU_MAM_NON_2,
    VietnameseSubject.NANG_KHIEU_QUAY_PHIM_TRUYEN_HINH,
    VietnameseSubject.NANG_KHIEU_SKDA_1,
    VietnameseSubject.NANG_KHIEU_SKDA_2,
    VietnameseSubject.NANG_KHIEU_TDTT,
    VietnameseSubject.NANG_KHIEU_THUYET_TRINH,
    VietnameseSubject.NANG_KHIEU_VE_1,
    VietnameseSubject.NANG_KHIEU_VE_2,
    VietnameseSubject.PHAT_TRIEN_CHU_DE_PHO_THO,
    VietnameseSubject.TU_DUY_GIAI_QUYET_NGU_VAN_DE,
    VietnameseSubject.VE_HINH_HOA,
    VietnameseSubject.VE_HINH_HOA_MY_THUAT,
    VietnameseSubject.VE_MY_THUAT,
    VietnameseSubject.VE_NANG_KHIEU,
    VietnameseSubject.VE_TRANG_TRI,
    VietnameseSubject.VE_TRANG_TRI_MAU,
    VietnameseSubject.XAY_DUNG_KICH_BAN_SU_KIEN
]
TalentSubject = Enum("TalentSubject", {item.name: item.value for item in NANG_KHIEU})

class NhomNganh(IntEnum):
    GIAO_DUC_DAO_TAO = 714
    NHAN_VAN = 722
    BAO_CHI_THONG_TIN = 732
    CONG_NGHE_THONG_TIN = 748
    KY_THUAT = 752
    NGHE_THUAT = 721
    KHOA_HOC_XA_HOI = 731
    KINH_DOANH = 734
    LUAT = 738
    KHOA_HOC_SU_SONG = 742
    KHOA_HOC_TU_NHIEN = 744
    THONG_KE = 746
    CONG_NGHE_KY_THUAT = 751
    SAN_XUAT_VA_CHE_BIEN = 754
    KIEN_TRUC = 758
    NONG_LAM_THUY_SAN = 762
    THU_Y = 764
    SUC_KHOE = 772
    DICH_VU_XA_HOI = 776
    DU_LICH = 781
    AN_NINH_QUOC_PHONG = 786
    MOI_TRUONG = 785
    VAN_TAI = 784
    OTHER = 790


class CCTA(StrEnum):
    CEFR = "CEFR"
    JLPT = "JLPT"


class CEFRLevel(StrEnum):
    A1 = "A1"
    A2 = "A2"
    B1 = "B1"
    B2 = "B2"
    C1 = "C1"
    C2 = "C2"


class JLPTLevel(StrEnum):
    N5 = "N5"
    N4 = "N4"
    N3 = "N3"
    N2 = "N2"
    N1 = "N1"
