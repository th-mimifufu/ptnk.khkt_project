from pydantic import BaseModel, Field, field_validator
from typing import List, Literal, Set, ClassVar, Optional, Dict, Union

from src.services.constants import TinhTP, HSGSubject, NhomNganh

_HSG_Field = Optional[Union[HSGSubject, Literal["0"]]]

class UserInputL1(BaseModel):
    cong_lap: int = Field(..., ge=0, le=1, description="1: Công lập, 0: Tư thục")
    tinh_tp: str = Field(..., description="Tỉnh/Thành phố (vd: TP. Hồ Chí Minh, ...)")
    hoc_phi: float = Field(..., ge=0, description="Mức học phí dự kiến (VNĐ/năm)")

    hsg_1: _HSG_Field = Field(None, description="Giải nhất HSG quốc gia (vd: Toán, Văn, Anh, ...)")
    hsg_2: _HSG_Field = Field(None, description="Giải nhì HSG quốc gia (vd: Toán, Văn, Anh, ...)")
    hsg_3: _HSG_Field = Field(None, description="Giải ba HSG quốc gia (vd: Toán, Văn, Anh, ...)")

    ahld: int = Field(0, ge=0, le=1, description="Anh hùng LLVT (1: Có, 0: Không)")
    dan_toc_thieu_so: int = Field(0, ge=0, le=1, description="Dân tộc thiểu số (1/0)")
    haimuoi_huyen_ngheo_tnb: int = Field(0, ge=0, le=1, description="50 huyện nghèo/TNB (1/0)")

    nhom_nganh: NhomNganh = Field(..., description="Nhóm ngành (vd: 714, 732, ...)")

    # --- Soft validators (Return [] nếu sai) ---
    _VALID_TINH_TP: ClassVar[Set[str]] = {e.value for e in TinhTP}

    @property
    def is_tinh_tp_valid(self) -> bool:
        return self.tinh_tp.strip() in self._VALID_TINH_TP
    
    @field_validator("tinh_tp", mode="before")
    @classmethod
    def norm_tinh_tp(cls, v): return str(v).strip() if v is not None else v

    # --- Hard validators (RAISE 422 nếu sai) ---
    @field_validator("cong_lap", mode="before")
    @classmethod
    def _coerce_cong_lap(cls, v):
        if v is None or str(v).strip() == "":
            raise ValueError("cong_lap is required (0 or 1)")
        iv = int(v)
        if iv not in (0, 1):
            raise ValueError("cong_lap must be 0 or 1")
        return iv
    
    @field_validator("hoc_phi", mode="before")
    @classmethod
    def _coerce_hoc_phi(cls, v):
        fv = float(v)
        if fv < 0:
            raise ValueError("hoc_phi must be >= 0")
        return fv
    
    @field_validator("hsg_1", "hsg_2", "hsg_3", mode="before")
    @classmethod
    def _norm_hsg(cls, v):
        if v is None:
            return None
        s = str(v).strip()
        if s == "" or s == "0":
            return "0"                
        return s 

    @field_validator("ahld", "dan_toc_thieu_so", "haimuoi_huyen_ngheo_tnb", mode="before")
    @classmethod
    def _coerce_flag(cls, v):
        iv = int(v)
        if iv not in (0, 1):
            raise ValueError("flag must be 0 or 1")
        return iv


class L1PredictResult(BaseModel):
    loai_uu_tien: str
    ma_xet_tuyen: Dict[str, float]

class L1BatchRequest(BaseModel):
    items: List[UserInputL1]