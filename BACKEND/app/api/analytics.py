from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.utils.exceptions import not_found

from app.services.inventory_analytics_service import (
    get_inventory_summary,
    get_low_stock,
    compute_risk_score,
)

router = APIRouter(prefix="/analytics", tags=["Analytics"])


# -----------------------------
# Inventory Summary
# -----------------------------
@router.get("/inventory")
def inventory_summary(db: Session = Depends(get_db)):
    data = get_inventory_summary(db)

    if not data:
        raise not_found("No inventory data available")

    return [
        {"blood_group": bg, "total_units": units}
        for bg, units in data
    ]


# -----------------------------
# Low Stock Alert
# -----------------------------
@router.get("/low-stock")
def low_stock(
    threshold: int = Query(5, gt=0),
    db: Session = Depends(get_db),
):
    data = get_low_stock(db, threshold)

    if not data:
        raise not_found("No blood groups below the threshold")

    return [
        {
            "blood_group": bg,
            "units_available": units
        }
        for bg, units in data
    ]

from fastapi import Query

@router.get("/risk", tags=["Analytics"])
def inventory_risk(
    blood_group: str = Query(..., description="Blood group (e.g. O+, A-)"),
    days: int = Query(7, gt=0, description="Days to analyze"),
    db: Session = Depends(get_db),
):
    """
    Predicts inventory risk based on recent depletion trends
    """
    return compute_risk_score(db, blood_group, days)
