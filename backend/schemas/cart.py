from pydantic import BaseModel
from typing import List

class CartItemBase(BaseModel):
    product_id: int
    quantity: int

class CartItemCreate(CartItemBase):
    user_id: int

class CartItem(CartItemBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class CartItemResponse(CartItem):
    name: str
    price: float

class CartItemUpdate(BaseModel):
    quantity: int

class BulkCartItemAdd(BaseModel):
    user_id: int
    items: List[dict] # list of {"name": "...", "quantity": ...}
