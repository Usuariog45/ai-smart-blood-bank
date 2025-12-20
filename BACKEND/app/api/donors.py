from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.donor import Donor
from app.schemas.donor import DonorCreate, DonorResponse
from app.utils.exceptions import conflict
from app.services.donor_ai import priority_score

router = APIRouter(
    prefix="/donors",
    tags=["Donors"]
)

@router.post("/", response_model=DonorResponse)
def register_donor(donor: DonorCreate, db: Session = Depends(get_db)):
    existing = db.query(Donor).filter(Donor.phone == donor.phone).first()
    if existing:
        raise conflict("Donor with this phone number already exists")

    new_donor = Donor(**donor.dict())
    db.add(new_donor)
    db.commit()
    db.refresh(new_donor)
    return new_donor


@router.get("/priority")
def get_priority_donors(
    blood_group: str = Query(...),
    lat: float = Query(...),
    lng: float = Query(...),
    db: Session = Depends(get_db)
):
    donors = db.query(Donor).filter(
    Donor.blood_group == blood_group,
    Donor.latitude.isnot(None),
    Donor.longitude.isnot(None)
    ).all()

    ranked = []
    for d in donors:
        score, distance = priority_score(d, blood_group, lat, lng)
        ranked.append({
            "id": d.id,
            "name": d.name,
            "blood_group": d.blood_group,
            "phone": d.phone,
            "city": d.city,
            "distance_km": distance,
            "priority_score": score
        })

    ranked.sort(key=lambda x: x["priority_score"], reverse=True)
    return ranked
