from sqlalchemy import Column, String, Text, JSON, Float
from .db import Base

class PatientCase(Base):
    __tablename__ = "cases"

    case_id = Column(String, primary_key=True, index=True)
    patient_id = Column(String, index=True)
    patient_name = Column(String)
    summary = Column(Text)

    lab_path = Column(JSON, nullable=True)       
    image_path = Column(String, nullable=True)

    soap = Column(JSON, nullable=True)           
    diagnoses = Column(JSON, nullable=True)
    treatment = Column(JSON, nullable=True)
    interpretations = Column(JSON, nullable=True)

    confidence = Column(Float, nullable=True)

    lab_data = Column(JSON, nullable=True)       
