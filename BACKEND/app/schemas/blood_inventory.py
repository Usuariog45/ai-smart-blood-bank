from pydantic import BaseModel


class BloodBankResult(BaseModel):
    blood_bank_id: int
    blood_bank_name: str
    blood_group: str
    units_available: int
    distance_km: float

    class Config:
        from_attributes = True
