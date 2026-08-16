from fastapi import APIRouter, HTTPException
from typing import List
from schemas.cart import CartItemCreate, CartItem, CartItemResponse, CartItemUpdate, BulkCartItemAdd

router = APIRouter()

# In-memory storage for MVP
carts_db = []
cart_id_counter = 1

# Mock product database for validation
PRODUCTS = {
    1: {"name": "Organic Bananas", "price": 2.99},
    2: {"name": "Almond Milk", "price": 4.49},
    3: {"name": "Whole Wheat Bread", "price": 3.99},
    4: {"name": "Rice", "price": 5.99},
    5: {"name": "Dal", "price": 3.49},
    6: {"name": "Butter", "price": 4.99},
    7: {"name": "Oats", "price": 4.99},
    8: {"name": "Milk", "price": 3.99},
    9: {"name": "Banana", "price": 1.99},
    10: {"name": "Tomato", "price": 2.49},
    11: {"name": "Cucumber", "price": 1.49},
    12: {"name": "Vegetables", "price": 5.49},
    13: {"name": "Wheat flour", "price": 6.99},
    14: {"name": "Spices", "price": 3.99},
    15: {"name": "Quinoa", "price": 7.99}
}

# Reverse mapping for bulk add by name
PRODUCT_NAME_TO_ID = {v["name"].lower(): k for k, v in PRODUCTS.items()}

@router.post("/", response_model=CartItem)
def add_to_cart(item: CartItemCreate):
    global cart_id_counter
    if item.product_id not in PRODUCTS:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if product already in cart
    for existing_item in carts_db:
        if existing_item["user_id"] == item.user_id and existing_item["product_id"] == item.product_id:
            existing_item["quantity"] += item.quantity
            return existing_item

    new_item = {
        "id": cart_id_counter,
        "user_id": item.user_id,
        "product_id": item.product_id,
        "quantity": item.quantity
    }
    carts_db.append(new_item)
    cart_id_counter += 1
    return new_item

@router.get("/{user_id}", response_model=List[CartItemResponse])
def get_cart(user_id: int):
    user_cart = []
    for item in carts_db:
        if item["user_id"] == user_id:
            prod = PRODUCTS.get(item["product_id"])
            if prod:
                user_cart.append({
                    **item,
                    "name": prod["name"],
                    "price": prod["price"]
                })
    return user_cart

@router.post("/bulk-add")
def bulk_add(payload: BulkCartItemAdd):
    global cart_id_counter
    added = []
    for i in payload.items:
        name_lower = i.get("name", "").lower()
        qty = i.get("quantity", 1)
        
        # Try finding exact match or partial match
        prod_id = PRODUCT_NAME_TO_ID.get(name_lower)
        if not prod_id:
            for k, v in PRODUCTS.items():
                if name_lower in v["name"].lower() or v["name"].lower() in name_lower:
                    prod_id = k
                    break
                    
        if not prod_id:
            prod_id = max(PRODUCTS.keys()) + 1 if PRODUCTS else 1
            PRODUCTS[prod_id] = {"name": i.get("name").title(), "price": 4.99}
            PRODUCT_NAME_TO_ID[name_lower] = prod_id
            
        if prod_id:
            # Check if exists
            found = False
            for existing in carts_db:
                if existing["user_id"] == payload.user_id and existing["product_id"] == prod_id:
                    existing["quantity"] += qty
                    if existing["quantity"] <= 0:
                        carts_db.remove(existing)
                    else:
                        added.append(existing)
                    found = True
                    break
            
            if not found and qty > 0:
                new_item = {
                    "id": cart_id_counter,
                    "user_id": payload.user_id,
                    "product_id": prod_id,
                    "quantity": qty
                }
                carts_db.append(new_item)
                cart_id_counter += 1
                added.append(new_item)
    return {"message": "Items added", "added": len(added)}

@router.put("/{user_id}/{product_id}")
def update_cart_item(user_id: int, product_id: int, update: CartItemUpdate):
    for item in carts_db:
        if item["user_id"] == user_id and item["product_id"] == product_id:
            item["quantity"] = update.quantity
            return item
    raise HTTPException(status_code=404, detail="Item not found in cart")

@router.delete("/{user_id}/{product_id}")
def remove_from_cart(user_id: int, product_id: int):
    global carts_db
    carts_db[:] = [item for item in carts_db if not (item["user_id"] == user_id and item["product_id"] == product_id)]
    return {"message": "Item removed"}
