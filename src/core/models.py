from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class L2UniRequirement(Base):
    __tablename__ = "l2_uni_requirement"
    id = Column(Integer, primary_key=True, autoincrement=True)
    uni_type_label = Column(Integer)
    province = Column(String)
    subject_combination = Column(String)
    score = Column(Float)
    tuition_fee = Column(Integer)
    certification_name = Column(String)
    certification_score = Column(String)
    certification_score_equivalence = Column(Float)
    conduct_grade_10 = Column(Integer)
    conduct_grade_11 = Column(Integer)
    conduct_grade_12 = Column(Integer)
    academic_performance_grade_10 = Column(Integer)
    academic_performance_grade_11 = Column(Integer)
    academic_performance_grade_12 = Column(Integer)
    major_code = Column(Integer)
    admission_code = Column(String)
    y_base = Column(Float)
    score_final = Column(Float)
    is_base_row = Column(Boolean)
