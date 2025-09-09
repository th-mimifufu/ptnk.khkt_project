from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List, Literal, Optional, Set, ClassVar, Union

from src.services.constants import TinhTP, NhomNganh

class Grade(BaseModel):
    toan: Optional[float] = Field(..., ge=0, le=10)
    ly: Optional[float] = Field(..., ge=0, le=10)
    hoa: Optional[float] = Field(..., ge=0, le=10)
    van: Optional[float] = Field(..., ge=0, le=10)
    anh: Optional[float] = Field(..., ge=0, le=10)
    sinh: Optional[float] = Field(None, ge=0, le=10)
    su: Optional[float] = Field(None, ge=0, le=10)
    dia: Optional[float] = Field(None, ge=0, le=10)
    tin: Optional[float] = Field(None, ge=0, le=10)
    gdkt_pl: Optional[float] = Field(None, ge=0, le=10)
    ve_tt: Optional[float] = Field(None, ge=0, le=10)
    ve_dt: Optional[float] = Field(None, ge=0, le=10)

class HocBa(BaseModel):
    grade_10: Grade
    grade_11: Grade
    grade_12: Grade

class AwardQG(BaseModel):
    subject: str = Field(..., description="Tên môn (Toán, Văn, Anh, ...)")
    level: int = Field(..., ge=1, le=4) 

class AwardEnglish(BaseModel):
    level: str = Field(..., pattern="^(A1|A2|B1|B2|C1|C2)$")

class UserInputL3(BaseModel):
    cong_lap: int = Field(..., ge=0, le=1, description="1: Công lập, 0: Tư thục")
    tinh_tp: str = Field(..., description="Tỉnh/Thành phố (vd: TP. Hồ Chí Minh, ...)")
    hoc_phi: float = Field(..., ge=0, description="Mức học phí dự kiến (VNĐ/năm)")
    hoc_ba: HocBa = Field(..., description="Điểm học bạ lớp 10, 11, 12")
    award_qg: Optional[AwardQG] = None
    award_english: Optional[AwardEnglish] = None
    nhom_nganh: NhomNganh = Field(..., description="Nhóm ngành (vd: 714, 732, ...)")

    _VALID_TINH_TP: ClassVar[Set[str]] = {e.value for e in TinhTP}

    @property
    def is_tinh_tp_valid(self) -> bool:
        return self.tinh_tp.strip() in self._VALID_TINH_TP
    
    @field_validator("tinh_tp", mode="before")
    @classmethod
    def norm_tinh_tp(cls, v): return str(v).strip() if v is not None else v

    @field_validator("cong_lap", mode="before")
    @classmethod
    def _v_cong_lap(cls, v):
        iv = int(v)
        if iv not in (0, 1):
            raise ValueError("cong_lap must be 0 or 1")
        return iv
    
class L3PredictResult(BaseModel):
    ma_xet_tuyen: str = Field(..., description="Mã xét tuyển")
    score: float = Field(..., description="Điểm xác suất model dự đoán mức độ phù hợp cho lựa chọn này")

class L3BatchRequest(BaseModel):
    items: List[UserInputL3]
