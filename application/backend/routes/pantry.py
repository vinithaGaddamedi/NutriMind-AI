from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

BARCODE_DB = {
    "0123456789": "Milk",
    "9876543210": "Rice",
    "1111222233": "Oats",
    "4444555566": "Quinoa"
}

class BarcodePayload(BaseModel):
    barcode: str

@router.post("/scan")
def scan_item(payload: BarcodePayload):
    barcode = payload.barcode
    item = BARCODE_DB.get(barcode, "Unknown Item")
    return {"item": item, "status": "success" if item != "Unknown Item" else "not_found"}
