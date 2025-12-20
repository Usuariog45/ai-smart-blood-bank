from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class InventoryLog(Base):
    __tablename__ = "inventory_logs"

    id = Column(Integer, primary_key=True, index=True)

    blood_bank_id = Column(
        Integer,
        ForeignKey("blood_banks.id"),
        nullable=False
    )

    blood_group = Column(String(5), nullable=False)

    change_type = Column(String(20), nullable=False)
    # values: INCREASE / DECREASE

    units_changed = Column(Integer, nullable=False)

    reason = Column(String(255), nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
