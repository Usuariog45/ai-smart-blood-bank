from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from app.models.inventory_log import InventoryLog
from app.models.blood_inventory import BloodInventory
from app.utils.exceptions import not_found


# -------------------------------------------------
# Inventory Summary
# -------------------------------------------------
def get_inventory_summary(db: Session):
    """
    Returns total available units per blood group
    """
    return (
        db.query(
            BloodInventory.blood_group,
            func.sum(BloodInventory.units_available),
        )
        .group_by(BloodInventory.blood_group)
        .all()
    )


# -------------------------------------------------
# Low Stock Detection
# -------------------------------------------------
def get_low_stock(db: Session, threshold: int):
    """
    Returns blood groups below threshold
    """
    return (
        db.query(
            BloodInventory.blood_group,
            BloodInventory.units_available,
        )
        .filter(BloodInventory.units_available <= threshold)
        .all()
    )


# -------------------------------------------------
# Risk Score Computation (Phase 4.3)
# -------------------------------------------------
def compute_risk_score(
    db: Session,
    blood_group: str,
    days: int,
):
    """
    Risk score based on recent inventory depletion trends
    """

    since_date = datetime.utcnow() - timedelta(days=days)

    logs = (
        db.query(InventoryLog)
        .filter(InventoryLog.blood_group == blood_group)
        .filter(InventoryLog.created_at >= since_date)
        .all()
    )

    if not logs:
        raise not_found("No inventory activity found for this blood group")

    total_depletion = 0

    for log in logs:
        if log.change_type == "DECREASE": # type:ignore 
            total_depletion += abs(log.units_changed) # type:ignore

    # Simple risk score logic
    risk_score = total_depletion / max(days, 1)

    if risk_score >= 5:
        risk_level = "HIGH"
    elif risk_score >= 2:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {
        "blood_group": blood_group,
        "days_analyzed": days,
        "total_depletion": total_depletion,
        "risk_score": round(risk_score, 2),
        "risk_level": risk_level,
    }
