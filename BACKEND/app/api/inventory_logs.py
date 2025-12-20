from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.inventory_log import InventoryLog
from app.schemas.inventory_log import InventoryLogResponse

router = APIRouter(
    prefix="/inventory/logs",
    tags=["Inventory Logs"]
)


@router.get("/", response_model=list[InventoryLogResponse])
def get_inventory_logs(db: Session = Depends(get_db)):
    return (
        db.query(InventoryLog)
        .order_by(InventoryLog.created_at.desc())
        .all()
    )
