from pydantic import BaseModel
from typing import Optional

class DonorCreate(BaseModel):
    name: str
    blood_group: str
    phone: str
    city: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]

class DonorResponse(DonorCreate):
    id: int

    class Config:
        from_attributes = True
