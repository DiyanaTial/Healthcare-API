from sqlalchemy import Column, Integer, String, Float, Date
from app.database import Base #connects it to database.py sqlalchemy

class HospitalMetric(Base):
    __tablename__ = "hospital_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(String)
    facility_name = Column(String)
    state = Column(String)
    measure_id = Column(String)
    measure_name = Column(String)
    score = Column(Float)
    start_date = Column(Date)
    end_date = Column(Date)
    