from fastapi import APIRouter, HTTPException
from typing import List
from schemas.order import OrderCreate, Order
from routes.cart import carts_db, PRODUCTS

router = APIRouter()

orders_db = []
order_id_counter = 1

@router.post("/", response_model=Order)
def create_order(order_req: OrderCreate):
    global order_id_counter
    user_cart = [item for item in carts_db if item["user_id"] == order_req.user_id]
    
    if not user_cart:
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    total_amount = 0
    order_items = []
    
    for item in user_cart:
        price = PRODUCTS[item["product_id"]]["price"]
        total_amount += price * item["quantity"]
        order_items.append({
            "product_id": item["product_id"],
            "quantity": item["quantity"],
            "price": price
        })
        
    new_order = {
        "id": order_id_counter,
        "user_id": order_req.user_id,
        "items": order_items,
        "total_amount": round(total_amount, 2),
        "status": "placed"
    }
    
    orders_db.append(new_order)
    order_id_counter += 1
    
    # Clear the user's cart
    carts_db[:] = [item for item in carts_db if item["user_id"] != order_req.user_id]
    
    return new_order

@router.get("/{user_id}", response_model=List[Order])
def get_orders(user_id: int):
    user_orders = [order for order in orders_db if order["user_id"] == user_id]
    return user_orders
