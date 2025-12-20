from sqlalchemy.orm import Session

from app.models.blood_inventory import BloodInventory
from app.models.inventory_log import InventoryLog
from app.utils.exceptions import bad_request


def update_inventory(
    *,
    db: Session,
    blood_bank_id: int,
    blood_group: str,
    units_change: int,
    change_type: str,
    reason: str | None = None,
):
    """
    Update blood inventory and create an audit log.

    units_change:
        +ve -> stock added
        -ve -> stock reduced
    """

    if units_change == 0:
        raise bad_request("Units change cannot be zero")

    # 1️⃣ Get inventory row (if exists)
    inventory = (
        db.query(BloodInventory)
        .filter(
            BloodInventory.blood_bank_id == blood_bank_id,
            BloodInventory.blood_group == blood_group,
        )
        .first()
    )

    # 2️⃣ If inventory does not exist, create it
    if not inventory:
        inventory = BloodInventory(
            blood_bank_id=blood_bank_id,
            blood_group=blood_group,
            units_available=0,
        )
        db.add(inventory)
        db.flush()  # ensures inventory.id is available

    # 3️⃣ Prevent negative stock
    if inventory.units_available + units_change < 0:
        raise bad_request("Insufficient stock to perform this operation")

    # 4️⃣ Update inventory
    inventory.units_available += units_change

    # 5️⃣ Create inventory audit log
    log = InventoryLog(
        blood_bank_id=blood_bank_id,
        blood_group=blood_group,
        change_type=change_type,
        units_changed=units_change,
        reason=reason,
    )

    db.add(log)

    # 6️⃣ Commit transaction
    db.commit()
    db.refresh(inventory)

    return inventory
