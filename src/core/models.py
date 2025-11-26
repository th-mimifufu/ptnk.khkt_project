from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class L2UniRequirement(Base):
    __tablename__ = "l2_uni_requirement"
    __table_args__ = {'schema': 'machine_learning'}
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

class Admission(Base):
    __tablename__ = "admissions"
    __table_args__ = {'schema': 'uni_guide'}
    id = Column(Integer, primary_key=True, autoincrement=True)
    major_code = Column(Integer)
    admission_code = Column(String)
    admission_type = Column(String)
    admission_type_name = Column(String)
    created_at = Column(String)
    major_name = Column(String)
    province = Column(String)
    study_program = Column(String)
    subject_combination = Column(String)
    tuition_fee = Column(Integer)
    uni_code = Column(String)
    uni_name = Column(String)
    uni_type = Column(Integer)
    uni_web_link = Column(String)
    updated_at = Column(String)


# class L3Transcript(Base):
#     __tablename__ = "l3_transcript"
#     __table_args__ = {'schema': 'machine_learning'}
#     created_at = Column(String)
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     major_code = Column(String)
#     major_group = Column(Integer)
#     major_name = Column(String)
#     province = Column(String)
#     score = Column(Float)
#     tuition_fee = Column(Integer)
#     uni_code = Column(String)
#     uni_type = Column(Integer)
#     updated_at = Column(String)

class L3Transcript(Base):
    __tablename__ = "l3_transcript_new"
    __table_args__ = {'schema': 'machine_learning'}
    created_at = Column(String)
    id = Column(Integer, primary_key=True)
    uni_code = Column(String)
    uni_name = Column(String)
    uni_web_link = Column(String)
    major_code = Column(String)
    major_group = Column(Integer)
    major_name = Column(String)
    province = Column(String)
    score = Column(Float)
    tuition_fee = Column(Integer)
    uni_type = Column(Integer)
    study_program = Column(String)
    admission_type = Column(String)
    admission_type_name = Column(String)
    admission_code = Column(String)
    updated_at = Column(String)

class TranscriptSujectGroup(Base):
    __tablename__ = "transcript_subject_group"
    __table_args__ = {'schema': 'machine_learning'}
    created_at = Column(String)
    id = Column(Integer, primary_key=True, autoincrement=True)
    major_code = Column(String)
    subject_combination = Column(String)
    uni_code = Column(String)
    updated_at = Column(String)