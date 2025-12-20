from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.blood_inventory import BloodInventory
from app.utils.deps import get_current_admin

router = APIRouter(prefix="/admin/inventory", tags=["Admin Inventory"])

@router.get("/")
def list_inventory(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return db.query(BloodInventory).all()
