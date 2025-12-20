from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer


class BloodInventory(Base):
    __tablename__ = "blood_inventory"

    id: Mapped[int] = mapped_column(primary_key=True)
    blood_bank_id: Mapped[int]
    blood_group: Mapped[str]
    units_available: Mapped[int] = mapped_column(Integer, default=0)
