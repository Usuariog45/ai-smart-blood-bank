from pydantic import BaseModel

class InventoryAnalytics(BaseModel):
    blood_group: str
    total_units: int
    
class LowStockAlert(BaseModel):
    blood_group: str
    units_available: int
