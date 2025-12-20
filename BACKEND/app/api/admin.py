from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.blood_bank import BloodBank
from app.schemas.blood_bank import BloodBankCreate
from app.utils.deps import get_current_admin

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/dashboard")
def admin_dashboard(admin=Depends(get_current_admin)):
    return {"message": f"Welcome admin {admin}"}

@router.get("/blood-banks")
def list_blood_banks(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return db.query(BloodBank).all()


@router.post("/blood-banks")
def create_blood_bank(
    data: BloodBankCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    bank = BloodBank(**data.dict())
    db.add(bank)
    db.commit()
    db.refresh(bank)
    return bank

from app.models.blood_inventory import BloodInventory

@router.post("/inventory")
def add_inventory(
    blood_bank_id: int,
    blood_group: str,
    units: int,
    db: Session = Depends(get_db)
):
    inventory = BloodInventory(
        blood_bank_id=blood_bank_id,
        blood_group=blood_group,
        units_available=units
    )
    db.add(inventory)
    db.commit()
    return {"status": "Inventory added"}

from app.models.blood_inventory import BloodInventory

from app.models.inventory_log import InventoryLog

@router.get("/inventory/logs")
def list_inventory_logs(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return db.query(InventoryLog).order_by(InventoryLog.created_at.desc()).all()


@router.put("/blood-banks/{bank_id}")
def update_blood_bank(
    bank_id: int,
    data: BloodBankCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    bank = db.query(BloodBank).get(bank_id)
    for k, v in data.dict().items():
        setattr(bank, k, v)
    db.commit()
    return bank


@router.delete("/blood-banks/{bank_id}")
def delete_blood_bank(
    bank_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    bank = db.query(BloodBank).get(bank_id)
    db.delete(bank)
    db.commit()
    return {"status": "deleted"}

from app.models.donation_camp import DonationCamp

@router.get("/camps")
def list_camps(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return db.query(DonationCamp).all()
