from pydantic import BaseModel, Field, validator
from typing import List, Optional
from enum import Enum

from src.services.l3.schemas import DGNL, HocBa, TNTHPTScores, PriorityRegion, PriorityObject

class CEFRLevel(str, Enum):
    B1 = "B1"
    B2 = "B2"
    C1 = "C1"
    C2 = "C2"

class AdmissionInputType1(BaseModel):
    """Input cho Đối tượng 1: Thí sinh CÓ kết quả ĐGNL"""
    dgnl_score: DGNL = Field(..., description="Điểm ĐGNL ĐHQG-HCM")
    tnthpt_scores: TNTHPTScores
    high_school_grades: HocBa
    # subject_combination: List[List[str]]  # List of subject combinations
    priority_region: PriorityRegion = Field(PriorityRegion.REGION_1)
    priority_object: PriorityObject = Field(PriorityObject.NORMAL)
    english_cert: Optional[CEFRLevel] = Field(None)

class AdmissionInputType2(BaseModel):
    """Input cho Đối tượng 2: Thí sinh KHÔNG CÓ kết quả ĐGNL"""
    tnthpt_scores: TNTHPTScores
    high_school_grades: HocBa
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

