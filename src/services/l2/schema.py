from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List, Literal, Optional, Set, ClassVar, Union

from src.services.constants import TinhTP, ToHopMon, CCTA, CEFRLevel, JLPTLevel, NhomNganh

CCTAName  = Union[CCTA, Literal["0"]]            
CCTALevel = Optional[Union[CEFRLevel, JLPTLevel, Literal["0"]]]

class UserInputL2(BaseModel):
    cong_lap: int = Field(..., ge=0, le=1, description="1: Công lập, 0: Tư thục")
    tinh_tp: str = Field(..., description="Tỉnh/Thành phố (vd: TP. Hồ Chí Minh, ...)")
    to_hop_mon: ToHopMon = Field(..., description="Tổ hợp môn (vd: D01, A00, VNUHCM, ...)")
    diem_chuan: float = Field(..., ge=0, description="Điểm thi thực tế hoặc điểm chuẩn user đạt được")
    hoc_phi: float = Field(..., ge=0, description="Mức học phí dự kiến (VNĐ/năm)")
    ten_ccta: str = Field(..., description="Tên chứng chỉ tiếng anh (nếu có)")
    diem_ccta: str = Field(..., description="Điểm chứng chỉ tiếng anh (nếu có)")
    hk10: int = Field(..., ge=1, le=4, description="Điểm rèn luyện năm lớp 10 (1: Tốt, 2: Khá, 3: Đạt, 4: Chưa đạt)")
    hk11: int = Field(..., ge=1, le=4, description="Điểm rèn luyện năm lớp 11 (1: Tốt, 2: Khá, 3: Đạt, 4: Chưa đạt)")
    hk12: int = Field(..., ge=1, le=4, description="Điểm rèn luyện năm lớp 12 (1: Tốt, 2: Khá, 3: Đạt, 4: Chưa đạt)")
    hl10: int = Field(..., ge=1, le=4, description="Điểm học lực năm lớp 10 (1: Tốt, 2: Khá, 3: Đạt, 4: Chưa đạt)")
    hl11: int = Field(..., ge=1, le=4, description="Điểm học lực năm lớp 11 (1: Tốt, 2: Khá, 3: Đạt, 4: Chưa đạt)")
    hl12: int = Field(..., ge=1, le=4, description="Điểm học lực năm lớp 12 (1: Tốt, 2: Khá, 3: Đạt, 4: Chưa đạt)")
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
    
    @field_validator("to_hop_mon", mode="before")
    @classmethod
    def norm_thm(cls, v): return str(v).strip().upper() if v is not None else v

    @field_validator("ten_ccta", mode="before")
    @classmethod
    def _norm_ccta_name(cls, v):
        if v is None: return "0"
        s = str(v).strip().upper()
        if s in {"", "0", "NONE", "NO"}: return "0"
        if s in {"CEFR", "JLPT"}: return s
        raise ValueError("ten_ccta must be '0', 'CEFR' or 'JLPT'")
    
    @field_validator("diem_ccta", mode="before")
    @classmethod
    def _norm_ccta_level(cls, v):
        if v is None: return "0"
        s = str(v).strip().upper()
        return "0" if s in {"", "0"} else s

    @model_validator(mode="after")
    def _pair_ccta_check(self):
        # nếu không có chứng chỉ -> level phải '0'
        if self.ten_ccta == "0":
            if self.diem_ccta not in (None, "0"):
                raise ValueError("diem_ccta must be '0' when ten_ccta is '0'")
            self.diem_ccta = "0"
            return self

        # có CEFR -> level phải thuộc CEFRLevel
        if self.ten_ccta == CCTA.CEFR:
            try:
                self.diem_ccta = CEFRLevel(str(self.diem_ccta))
            except Exception:
                raise ValueError("diem_ccta must be one of CEFR levels: A1,A2,B1,B2,C1,C2")
            return self

        # có JLPT -> level phải thuộc JLPTLevel
        if self.ten_ccta == CCTA.JLPT:
            try:
                self.diem_ccta = JLPTLevel(str(self.diem_ccta))
            except Exception:
                raise ValueError("diem_ccta must be one of JLPT levels: N5,N4,N3,N2,N1")
            return self
        return self
    
class L2PredictResult(BaseModel):
    ma_xet_tuyen: str = Field(..., description="Mã xét tuyển")
    score: float = Field(..., description="Điểm xác suất model dự đoán mức độ phù hợp cho lựa chọn này")

class L2BatchRequest(BaseModel):
    items: List[UserInputL2]
