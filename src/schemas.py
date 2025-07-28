from pydantic import BaseModel, Field
from typing import Optional

class UserInput(BaseModel):
    to_hop_mon: str = Field(..., description="Tổ hợp môn (vd: D01, A00, VNUHCM, ...)")
    diem_chuan: float = Field(..., description="Điểm thi thực tế hoặc điểm chuẩn user đạt được")
    hoc_phi: float = Field(..., description="Mức học phí dự kiến của ngành/trường (đơn vị: VNĐ/năm)")
    ten_ccta: str = Field(..., description="Tên chứng chỉ tiếng anh (nếu có)")
    diem_ccta: str = Field(..., description="Điểm chứng chỉ tiếng anh (nếu có)")
    diem_quy_doi: float = Field(..., description="Điểm quy đổi (nếu có) từ các chứng chỉ tiếng anh")
    hk10: int = Field(..., description="Điểm trung bình học kỳ năm lớp 10")
    hk11: int = Field(..., description="Điểm trung bình học kỳ năm lớp 11")
    hk12: int = Field(..., description="Điểm trung bình học kỳ năm lớp 12")
    hl10: int = Field(..., description="Học lực lớp 10")
    hl11: float = Field(..., description="Học lực lớp 11")
    hl12: float = Field(..., description="Học lực lớp 12")
    nhom_nganh: float = Field(..., description="Nhóm ngành")

class PredictResult(BaseModel):
    ma_xet_tuyen: str = Field(..., description="Mã xét tuyển")
    score: float = Field(..., description="Điểm xác suất model dự đoán mức độ phù hợp cho lựa chọn này")
