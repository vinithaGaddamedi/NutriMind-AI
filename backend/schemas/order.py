from pydantic import BaseModel
from typing import List

class OrderItem(BaseModel):
    product_id: int
    quantity: int
    price: float

class OrderCreate(BaseModel):
    user_id: int

class Order(BaseModel):
    id: int
    user_id: int
    items: List[OrderItem]
    total_amount: float
    status: str

    class Config:
        from_attributes = True
