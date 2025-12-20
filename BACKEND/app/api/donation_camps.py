from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.database import get_db
from app.models.donation_camp import DonationCamp
from app.schemas.donation_camp import DonationCampCreate, DonationCampResponse

router = APIRouter(
    prefix="/camps",
    tags=["Donation Camps"]
)

@router.post("/", response_model=DonationCampResponse)
def create_camp(camp: DonationCampCreate, db: Session = Depends(get_db)):
    new_camp = DonationCamp(**camp.dict())
    db.add(new_camp)
    db.commit()
    db.refresh(new_camp)
    return new_camp

@router.get("/", response_model=list[DonationCampResponse])
def list_upcoming_camps(db: Session = Depends(get_db)):
    return (
        db.query(DonationCamp)
        .filter(DonationCamp.camp_date >= datetime.utcnow(),
                DonationCamp.is_active == True)
        .all()
    )
