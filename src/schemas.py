from pydantic import BaseModel, Field
from typing import Dict, Optional

class UserInputL1(BaseModel):
    cong_lap: int = Field(..., description="1: Công lập, 0: Tư thục")
    tinh_tp: str = Field(..., description="Tỉnh/Thành phố (vd: TP. Hồ Chí Minh, ...)")
    hoc_phi: float = Field(..., description="Mức học phí dự kiến của ngành (đơn vị: VNĐ/năm)")
    hsg_1: str = Field(..., description="Môn học sinh giỏi 1 (vd: Toán, Văn, Anh, ...)")
    hsg_2: Optional[str] = Field(None, description="Môn học sinh giỏi 2 (vd: Toán, Văn, Anh, ...)")
    hsg_3: Optional[str] = Field(None, description="Môn học sinh giỏi 3 (vd: Toán, Văn, Anh, ...)")
    ahld: Optional[str] = Field(None, description="Anh hùng lực lượng vũ trang (1: Có, 0: Không)")
    dan_toc_thieu_so: Optional[str] = Field(None, description="Dân tộc thiểu số (1: Có, 0: Không)")
    haimuoi_huyen_ngheo_tnb: Optional[str] = Field(None, description="Hộ nghèo, hải đảo, huyện nghèo, tỉnh nghèo (1: Có, 0: Không)")
    nhom_nganh: int = Field(..., description="Nhóm ngành (vd: 714, 732, ...)")

class UserInputL2(BaseModel):
    cong_lap: int = Field(..., description="1: Công lập, 0: Tư thục")
    tinh_tp: str = Field(..., description="Tỉnh/Thành phố (vd: TP. Hồ Chí Minh, ...)")
    to_hop_mon: str = Field(..., description="Tổ hợp môn (vd: D01, A00, VNUHCM, ...)")
    diem_chuan: float = Field(..., description="Điểm thi thực tế hoặc điểm chuẩn user đạt được")
    hoc_phi: float = Field(..., description="Mức học phí dự kiến của ngành (đơn vị: VNĐ/năm)")
    ten_ccta: str = Field(..., description="Tên chứng chỉ tiếng anh (nếu có)")
    diem_ccta: str = Field(..., description="Điểm chứng chỉ tiếng anh (nếu có)")
    hk10: int = Field(..., description="Điểm trung bình học kỳ năm lớp 10 (1: Giỏi, 2: Khá, 3: Trung bình, 4: Yếu)")
    hk11: int = Field(..., description="Điểm trung bình học kỳ năm lớp 11 (1: Giỏi, 2: Khá, 3: Trung bình, 4: Yếu)")
    hk12: int = Field(..., description="Điểm trung bình học kỳ năm lớp 12 (1: Giỏi, 2: Khá, 3: Trung bình, 4: Yếu)")
    hl10: int = Field(..., description="Học lực lớp 10 (1: Giỏi, 2: Khá, 3: Trung bình, 4: Yếu)")
    hl11: int = Field(..., description="Học lực lớp 11 (1: Giỏi, 2: Khá, 3: Trung bình, 4: Yếu)")
    hl12: int = Field(..., description="Học lực lớp 12 (1: Giỏi (trên 8), 2: Trên 7, 3: Khá, 4: Trung bình, 5: Yếu)")
    nhom_nganh: int = Field(..., description="Nhóm ngành (vd: 714, 732, ...)")

class L1PredictResult(BaseModel):
    loai_uu_tien: str
    ma_xet_tuyen: Dict[str, float]

class L2PredictResult(BaseModel):
    ma_xet_tuyen: str = Field(..., description="Mã xét tuyển")
    score: float = Field(..., description="Điểm xác suất model dự đoán mức độ phù hợp cho lựa chọn này")
