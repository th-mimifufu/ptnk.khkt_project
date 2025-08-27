from pydantic import BaseModel, Field, field_validator
from typing import Set, ClassVar

from src.services.constants import TinhTP

class UserInputL2(BaseModel):
    cong_lap: int = Field(..., description="1: Công lập, 0: Tư thục")
    tinh_tp: str = Field(..., description="Tỉnh/Thành phố (vd: TP. Hồ Chí Minh, ...)")
    to_hop_mon: str = Field(..., description="Tổ hợp môn (vd: D01, A00, VNUHCM, ...)")
    diem_chuan: float = Field(..., description="Điểm thi thực tế hoặc điểm chuẩn user đạt được")
    hoc_phi: float = Field(..., description="Mức học phí dự kiến của ngành (đơn vị: VNĐ/năm)")
    ten_ccta: str = Field(..., description="Tên chứng chỉ tiếng anh (nếu có)")
    diem_ccta: str = Field(..., description="Điểm chứng chỉ tiếng anh (nếu có)")
    hk10: int = Field(..., description="Điểm rèn luyện năm lớp 10 (1: Tốt, 2: Khá, 3: Đạt, 4: Chưa đạt)")
    hk11: int = Field(..., description="Điểm rèn luyện năm lớp 11 (1: Tốt, 2: Khá, 3: Đạt, 4: Chưa đạt)")
    hk12: int = Field(..., description="Điểm rèn luyện năm lớp 12 (1: Tốt, 2: Khá, 3: Đạt, 4: Chưa đạt)")
    hl10: int = Field(..., description="Điểm học lực năm lớp 10 (1: Tốt, 2: Khá, 3: Đạt, 4: Chưa đạt)")
    hl11: int = Field(..., description="Điểm học lực năm lớp 11 (1: Tốt, 2: Khá, 3: Đạt, 4: Chưa đạt)")
    hl12: int = Field(..., description="Điểm học lực năm lớp 12 (1: Tốt, 2: Khá, 3: Đạt, 4: Chưa đạt)")
    nhom_nganh: int = Field(..., description="Nhóm ngành (vd: 714, 732, ...)")

    _VALID_TINH_TP: ClassVar[Set[str]] = {e.value for e in TinhTP}

    @property
    def is_tinh_tp_valid(self) -> bool:
        return self.tinh_tp.strip() in self._VALID_TINH_TP
    
    @field_validator("tinh_tp", mode="before")
    @classmethod
    def norm_tinh_tp(cls, v): return str(v).strip() if v is not None else v

    @field_validator("to_hop_mon", mode="before")
    @classmethod
    def norm_thm(cls, v): return str(v).strip().upper() if v is not None else v

class L2PredictResult(BaseModel):
    ma_xet_tuyen: str = Field(..., description="Mã xét tuyển")
    score: float = Field(..., description="Điểm xác suất model dự đoán mức độ phù hợp cho lựa chọn này")
