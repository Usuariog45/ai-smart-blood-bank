from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.blood_inventory import BloodInventory
from app.models.blood_bank import BloodBank
from app.schemas.blood_inventory import BloodBankResult
from app.services.distance_service import haversine_distance
from app.utils.exceptions import not_found, bad_request

router = APIRouter(prefix="/blood", tags=["Find Blood"])


@router.get("/search", response_model=list[BloodBankResult])
def search_blood(
    blood_group: str = Query(...),
    lat: float = Query(...),
    lng: float = Query(...),
    radius_km: float = Query(10),
    db: Session = Depends(get_db),
):

    if radius_km <= 0:
        raise bad_request("Radius must be greater than 0 km")

    # 2️⃣ Fetch matching inventories
    inventories = (
        db.query(BloodInventory, BloodBank)
        .join(BloodBank, BloodInventory.blood_bank_id == BloodBank.id)
        .filter(BloodInventory.blood_group == blood_group)
        .filter(BloodInventory.units_available > 0)
        .filter(BloodBank.is_active == True)
        .all()
    )

    if not inventories:
        raise not_found("No blood banks found for the given criteria")

    results = []

    for inventory, bank in inventories:
        distance = haversine_distance(
            lat, lng, bank.latitude, bank.longitude
        )

        if distance <= radius_km:
            results.append(
                BloodBankResult(
                    blood_bank_id=bank.id,
                    blood_bank_name=bank.name,
                    blood_group=inventory.blood_group,
                    units_available=inventory.units_available,
                    distance_km=round(distance, 2),
                )
            )

    if not results:
        raise not_found("No blood banks found within the given radius")

  
    return sorted(results, key=lambda x: x.distance_km)
