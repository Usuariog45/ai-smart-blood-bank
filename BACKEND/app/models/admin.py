from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    blood_bank_id = Column(Integer, ForeignKey("blood_banks.id"))
    username = Column(String(50), unique=True)
    password_hash = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
