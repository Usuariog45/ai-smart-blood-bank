from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.blood_bank import BloodBank
from app.utils.deps import get_current_admin

router = APIRouter(prefix="/admin/blood-banks", tags=["Admin Blood Banks"])

@router.get("/")
def list_blood_banks(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return db.query(BloodBank).all()


@router.post("/")
def create_blood_bank(
    name: str,
    city: str,
    latitude: float,
    longitude: float,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    bank = BloodBank(
        name=name,
        city=city,
        latitude=latitude,
        longitude=longitude
    )
    db.add(bank)
    db.commit()
    db.refresh(bank)
    return bank
