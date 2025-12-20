from pydantic import BaseModel
from datetime import datetime


class InventoryLogResponse(BaseModel):
    blood_bank_id: int
    blood_group: str
    change_type: str
    units_changed: int    
    reason: str | None
    created_at: datetime

