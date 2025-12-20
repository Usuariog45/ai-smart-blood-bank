from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class BloodBank(Base):
    __tablename__ = "blood_banks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    address = Column(String(255))
    city = Column(String(50), index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    contact_number = Column(String(15))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
