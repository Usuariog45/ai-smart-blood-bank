from pydantic import BaseModel

class BloodBankCreate(BaseModel):
    name: str
    city: str
    latitude: float
    longitude: float
