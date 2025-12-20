from pydantic import BaseModel
from datetime import datetime

class DonationCampCreate(BaseModel):
    name: str
    city: str
    latitude: float
    longitude: float
    camp_date: datetime

class DonationCampResponse(DonationCampCreate):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
