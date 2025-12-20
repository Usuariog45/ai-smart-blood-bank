from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class Donor(Base):
    __tablename__ = "donors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    blood_group = Column(String(5), index=True, nullable=False)
    phone = Column(String(15), unique=True, nullable=False)
    city = Column(String(100))
    latitude = Column(Float)
    longitude = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
