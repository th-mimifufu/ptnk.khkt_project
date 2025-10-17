from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional
from enum import Enum
import math

class CEFRLevel(str, Enum):
    B1 = "B1"
    B2 = "B2"
    C1 = "C1"
    C2 = "C2"

class SubjectCombination(str, Enum):
    A00 = "A00"  # Toán, Lý, Hóa
    A01 = "A01"  # Toán, Lý, Anh
    B00 = "B00"  # Toán, Hóa, Sinh
    D01 = "D01"  # Toán, Văn, Anh
    X06 = "X06"  # Toán, Tin, Anh
    X07 = "X07"  # Toán, Lý, Tin
    X08 = "X08"  # Toán, Hóa, Tin

class PriorityRegion(float, Enum):
    REGION_1 = 0.75   # Khu vực 1
    REGION_2 = 0.25    # Khu vực 2
    REGION_3 = 0.0    # Khu vực 3

class PriorityObject(float, Enum):
    NORMAL = 0.0      # Không ưu tiên
    OBJECT_1 = 2.0    # Đối tượng 1
    OBJECT_2 = 1.0    # Đối tượng 2

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
    cong_nghe: Optional[float] = Field(None, ge=0, le=10)

class HighSchoolTranscript(BaseModel):
    """Điểm học bạ THPT"""
    grade_10: Grade = Field(..., description="Điểm lớp 10")
    grade_11: Grade = Field(..., description="Điểm lớp 11")
    grade_12: Grade = Field(..., description="Điểm lớp 12")

class SubjectScores(BaseModel):
    subject_name: str = Field(..., description="Tên môn học")
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

class DGNL(BaseModel):
    language_score: int = Field(..., ge=0, le=400,description="Điểm phần sử dụng ngôn ngữ)")
    math_score: int = Field(..., ge=0, le=300, description="Điểm phần toán học")
    science_logic: int = Field(..., ge=0, le=500, description="Điểm phần tư duy khoa học")

class AdmissionInputType1(BaseModel):
    """Input cho Đối tượng 1: Thí sinh CÓ kết quả ĐGNL"""
    dgnl_score: DGNL = Field(..., description="Điểm ĐGNL ĐHQG-HCM")
    tnthpt_scores: TNTHPTScores
    high_school_grades: HighSchoolTranscript
    # subject_combination: List[List[str]]  # List of subject combinations
    priority_region: PriorityRegion = Field(PriorityRegion.REGION_1)
    priority_object: PriorityObject = Field(PriorityObject.NORMAL)
    english_cert: Optional[CEFRLevel] = Field(None)

class AdmissionInputType2(BaseModel):
    """Input cho Đối tượng 2: Thí sinh KHÔNG CÓ kết quả ĐGNL"""
    tnthpt_scores: TNTHPTScores
    high_school_grades: HighSchoolTranscript
    # subject_combination: List[List[str]]
    priority_region: PriorityRegion = Field(PriorityRegion.REGION_1)
    priority_object: PriorityObject = Field(PriorityObject.NORMAL)
    english_cert: Optional[CEFRLevel] = Field(None)

class AdmissionResult(BaseModel):
    """Kết quả tính điểm xét tuyển"""
    ma_nganh: str = Field(..., description="Mã ngành")
    ten_nganh: str = Field(..., description="Tên ngành")
    diem_chuan: float = Field(..., description="Điểm chuẩn của ngành")
    nhom_nganh: int = Field(..., description="Nhóm ngành")
    best_to_hop: List[str] = Field(..., description="Tổ hợp môn tốt nhất")
    best_to_hop_score: float = Field(..., description="Điểm tổ hợp môn tốt nhất")
    bonus_points: float = Field(..., description="Điểm ưu tiên/thưởng")
    total_score: float = Field(..., description="Tổng điểm cuối cùng")
    
    class Config:
        json_encoders = {
            float: lambda v: round(v, 2)
        }

