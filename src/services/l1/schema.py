from pydantic import BaseModel, Field, field_validator
from typing import Set, ClassVar, Optional, Dict

from src.services.constants import TinhTP

class UserInputL1(BaseModel):
    cong_lap: int = Field(..., description="1: Công lập, 0: Tư thục")
    tinh_tp: str = Field(..., description="Tỉnh/Thành phố (vd: TP. Hồ Chí Minh, ...)")
    hoc_phi: float = Field(..., description="Mức học phí dự kiến của ngành (đơn vị: VNĐ/năm)")
    hsg_1: Optional[str] = Field(None, description="Giải nhất HSG quốc gia (vd: Toán, Văn, Anh, ...)")
    hsg_2: Optional[str] = Field(None, description="Giải nhì HSG quốc gia (vd: Toán, Văn, Anh, ...)")
    hsg_3: Optional[str] = Field(None, description="Giải ba HSG quốc gia (vd: Toán, Văn, Anh, ...)")
    ahld: Optional[str] = Field(None, description="Anh hùng lực lượng vũ trang (1: Có, 0: Không)")
    dan_toc_thieu_so: Optional[str] = Field(None, description="Dân tộc thiểu số (1: Có, 0: Không)")
    haimuoi_huyen_ngheo_tnb: Optional[str] = Field(None, description="Hộ nghèo, hải đảo, huyện nghèo, tỉnh nghèo (1: Có, 0: Không)")
    nhom_nganh: int = Field(..., description="Nhóm ngành (vd: 714, 732, ...)")

    _VALID_TINH_TP: ClassVar[Set[str]] = {e.value for e in TinhTP}

    @property
    def is_tinh_tp_valid(self) -> bool:
        return self.tinh_tp.strip() in self._VALID_TINH_TP
    
    @field_validator("tinh_tp", mode="before")
    @classmethod
    def norm_tinh_tp(cls, v): return str(v).strip() if v is not None else v

class L1PredictResult(BaseModel):
    loai_uu_tien: str
    ma_xet_tuyen: Dict[str, float]