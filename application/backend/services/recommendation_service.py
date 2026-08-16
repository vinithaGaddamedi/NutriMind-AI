from routes.order import orders_db
from routes.cart import PRODUCTS

def get_recommendations(user_id: int):
    user_orders = [order for order in orders_db if order["user_id"] == user_id]
    
    purchased_product_ids = set()
    for order in user_orders:
        for item in order["items"]:
            purchased_product_ids.add(item["product_id"])
            
    recommendations = []
    
    # Simple AI Rule-Based logic
    # If user bought "Rice" (4) -> suggest "Dal" (5)
    if 4 in purchased_product_ids and 5 not in purchased_product_ids:
        recommendations.append({"product_id": 5, "name": PRODUCTS[5]["name"], "reason": "Because you bought Rice"})
        
    # If "Whole Wheat Bread" (3) -> suggest "Butter" (6)
    if 3 in purchased_product_ids and 6 not in purchased_product_ids:
        recommendations.append({"product_id": 6, "name": PRODUCTS[6]["name"], "reason": "Because you bought Bread"})
        
    # Default fallback recommendations if empty
    if not recommendations:
        recommendations = [
            {"product_id": 1, "name": PRODUCTS[1]["name"], "reason": "Popular choice"},
            {"product_id": 2, "name": PRODUCTS[2]["name"], "reason": "Healthy option"}
        ]
        
    return recommendations
