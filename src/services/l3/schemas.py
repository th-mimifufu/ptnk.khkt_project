from pydantic import BaseModel, Field, field_validator, validator
from typing import Dict, List, Literal, Optional, Set, ClassVar
from enum import Enum
from src.services.constants1 import TinhTP, NhomNganh, HSGSubject, CEFRLevel, SubjectName
class PriorityRegion(float, Enum):
    REGION_1 = 0.75
    REGION_2 = 0.25
    REGION_3 = 0.0

class PriorityObject(float, Enum):
    NORMAL = 0.0
    OBJECT_1 = 2.0
    OBJECT_2 = 1.0

class Grade(BaseModel):
    """Điểm học bạ - chỉ chứa các môn học chính"""
    toan: float = Field(..., ge=0, le=10)
    ly: float = Field(..., ge=0, le=10)
    hoa: float = Field(..., ge=0, le=10)
    van: float = Field(..., ge=0, le=10)
    anh: float = Field(..., ge=0, le=10)
    sinh: float = Field(..., ge=0, le=10)
    su: float = Field(..., ge=0, le=10)
    dia: float = Field(..., ge=0, le=10)
    tin: float = Field(..., ge=0, le=10)
    gdkt_pl: float = Field(..., ge=0, le=10)
    cong_nghe: float = Field(..., ge=0, le=10)

# class NangKhieuAmNhac1(BaseModel):
#     """Năng khiếu Âm nhạc 1: Hát và Xướng âm"""
#     hat_va_xuong_am: Optional[float] = Field(None, ge=0, le=10, description="Điểm hát và xướng âm")

# class NangKhieuAmNhac2(BaseModel):
#     """Năng khiếu Âm nhạc 2: Thanh nhạc hoặc Nhạc cụ"""
#     thanh_nhac: Optional[float] = Field(None, ge=0, le=10, description="Điểm thanh nhạc (hát có thể kết hợp nhạc cụ)")
#     nhac_cu: Optional[float] = Field(None, ge=0, le=10, description="Điểm nhạc cụ (hát và đàn)")

class NangKhieuKhoiT(BaseModel):
    """Điểm năng khiếu khối T (Thể thao)"""
    tdtt: Optional[float] = Field(None, ge=0, le=10, description="Điểm thể dục thể thao")

class NangKhieuKhoiM(BaseModel):
    """Điểm năng khiếu khối M"""
    doc_dien_cam: Optional[float] = Field(None, ge=0, le=10, description="Điểm đọc diễn cảm")
    hat: Optional[float] = Field(None, ge=0, le=10, description="Điểm hát")

class NangKhieuKhoiN(BaseModel):
    """Điểm năng khiếu khối N"""
    # Âm nhạc cụ thể
    nang_khieu_am_nhac_1: Optional[float] = Field(None, ge=0, le=10, description="Năng khiếu Âm nhạc 1")
    nang_khieu_am_nhac_2: Optional[float] = Field(None, ge=0, le=10, description="Năng khiếu Âm nhạc 2")
    
    # Các loại khác
    xuong_am: Optional[float] = Field(None, ge=0, le=10, description="Điểm xướng âm")
    bieu_dien_nghe_thuat: Optional[float] = Field(None, ge=0, le=10, description="Điểm biểu diễn nghệ thuật")
    ky_xuong_am: Optional[float] = Field(None, ge=0, le=10, description="Điểm ký xướng âm")
    hat_hoac_bieu_dien_nhac_cu: Optional[float] = Field(None, ge=0, le=10, description="Điểm hát hoặc biểu diễn nhạc cụ")
    xay_dung_kich_ban_su_kien: Optional[float] = Field(None, ge=0, le=10, description="Điểm xây dựng kịch bản sự kiện")
    
    # Năng khiếu chung (cho N05)
    nang_khieu_chung: Optional[float] = Field(None, ge=0, le=10, description="Điểm năng khiếu chung")

class NangKhieu(BaseModel):
    """Điểm năng khiếu - tách riêng khỏi Grade"""
    # Năng khiếu mỹ thuật
    ve_tt: Optional[float] = Field(None, ge=0, le=10, description="Điểm vẽ trang trí")
    ve_dt: Optional[float] = Field(None, ge=0, le=10, description="Điểm vẽ mỹ thuật")
    ve_nk: Optional[float] = Field(None, ge=0, le=10, description="Điểm vẽ năng khiếu")
    
    # Năng khiếu âm nhạc và biểu diễn
    hat: Optional[float] = Field(None, ge=0, le=10, description="Điểm hát")
    hat_mua: Optional[float] = Field(None, ge=0, le=10, description="Điểm hát-múa")
    doc_dien_cam: Optional[float] = Field(None, ge=0, le=10, description="Điểm đọc diễn cảm")
    
    # Năng khiếu báo chí
    nang_khieu_bao_chi: Optional[float] = Field(None, ge=0, le=10, description="Điểm năng khiếu báo chí")
    
    # Năng khiếu theo khối
    nang_khieu_M: Optional[NangKhieuKhoiM] = None
    nang_khieu_N: Optional[NangKhieuKhoiN] = None
    nang_khieu_T: Optional[NangKhieuKhoiT] = None

class HocBa(BaseModel):
    """Học bạ 3 năm THPT"""
    grade_10: Grade
    grade_11: Grade
    grade_12: Grade

class AwardQG(BaseModel):
    subject: HSGSubject = Field(..., description="Tên môn (Toán, Văn, Anh, ...)")
    level: int = Field(..., ge=1, le=4) 

class AwardEnglish(BaseModel):
    level: CEFRLevel = Field(..., description="Chứng chỉ tiếng anh")

InterCertLiteral = Literal[
    "A_Level",
    "ACT",
    "Duolingo_English_Test",
    "IB",
    "OSSD",
    "PTE_Academic",
    "SAT",
]

class InterCer(BaseModel):
    name: InterCertLiteral = Field(..., description="Tên chứng chỉ (SAT, IB, ...)")
    score: str = Field(..., description="Điểm số chứng chỉ")

class DGNL(BaseModel):
    language_score: int = Field(..., ge=0, le=400, description="Điểm phần sử dụng ngôn ngữ")
    math_score: int = Field(..., ge=0, le=300, description="Điểm phần toán học")
    science_logic: int = Field(..., ge=0, le=500, description="Điểm phần tư duy khoa học")
class SubjectScores(BaseModel):
    subject_name: SubjectName = Field(..., description="Tên môn học")
    score: float = Field(..., ge=0, le=10, description="Điểm môn học")

class TNTHPTScores(BaseModel):
    """Điểm thi tốt nghiệp THPT"""
    math_score: SubjectScores = Field(
        default_factory=lambda: SubjectScores(subject_name="Toán", score=0),
        description="Điểm Toán"
    )
    literature_score: SubjectScores = Field(
        default_factory=lambda: SubjectScores(subject_name="Văn", score=0),
        description="Điểm Văn"
    )
    elective_1_score: SubjectScores = Field(..., description="Điểm môn tự chọn 1")
    elective_2_score: SubjectScores = Field(..., description="Điểm môn tự chọn 2")

    @validator("math_score", pre=True, always=True)
    def set_math_subject_name(cls, v):
        if isinstance(v, dict):
            v["subject_name"] = "Toán"
            return v
        if isinstance(v, SubjectScores):
            v.subject_name = "Toán"
            return v
        return v

    @validator("literature_score", pre=True, always=True)
    def set_literature_subject_name(cls, v):
        if isinstance(v, dict):
            v["subject_name"] = "Văn"
            return v
        if isinstance(v, SubjectScores):
            v.subject_name = "Văn"
            return v
        return v
class UserInputL3(BaseModel):
    """Input chính cho L3 với NangKhieu tách riêng"""
    cong_lap: int = Field(..., ge=0, le=1, description="1: Công lập, 0: Tư thục")
    tinh_tp: str = Field(..., description="Tỉnh/Thành phố (vd: TP. Hồ Chí Minh, ...)")
    hoc_phi: float = Field(..., ge=0, description="Mức học phí dự kiến (VNĐ/năm)")
    hoc_ba: HocBa = Field(..., description="Điểm học bạ lớp 10, 11, 12")
    nang_khieu: Optional[NangKhieu] = None
    award_qg: Optional[List[AwardQG]] = None
    award_english: Optional[AwardEnglish] = None
    int_cer: Optional[InterCer] = Field(None, description="Chứng chỉ quốc tế (vd: SAT, IB, ...)")
    dgnl: Optional[DGNL] = Field(None, description="Điểm đánh giá năng lực (nếu có)")
    thpt: Optional[TNTHPTScores] = Field(None, description="Điểm thi tốt nghiệp THPT (nếu có)")
    nhom_nganh: NhomNganh = Field(..., description="Nhóm ngành (vd: 714, 732, ...)")
    priority_region: PriorityRegion = Field(PriorityRegion.REGION_3, description="Khu vực ưu tiên")
    priority_object: PriorityObject = Field(PriorityObject.NORMAL, description="Đối tượng ưu tiên")

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

class UniversityResult(BaseModel):
    ma_nganh: str
    ten_nganh: str
    diem_chuan: float
    nhom_nganh: int
    best_to_hop: List[str]
    best_to_hop_score: float
    bonus_points: float
    total_score: float

class L3PredictResult(BaseModel):
    result: Dict[str, List[UniversityResult]]

class L3BatchRequest(BaseModel):
    items: List[UserInputL3]