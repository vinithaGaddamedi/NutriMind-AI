PRICE_DB = {
    "walmart": {
        "Rice": 5, "Milk": 3, "Banana": 2, "Dal": 4, 
        "Oats": 4, "Tomato": 2, "Cucumber": 1, "Vegetables": 5, 
        "Wheat flour": 6, "Spices": 4, "Quinoa": 7
    },
    "costco": {
        "Rice": 4, "Milk": 4, "Banana": 3, "Dal": 5, 
        "Oats": 3, "Tomato": 3, "Cucumber": 2, "Vegetables": 4, 
        "Wheat flour": 5, "Spices": 5, "Quinoa": 6
    },
    "amazon_fresh": {
        "Rice": 6, "Milk": 3, "Banana": 2, "Dal": 4, 
        "Oats": 5, "Tomato": 2, "Cucumber": 1, "Vegetables": 6, 
        "Wheat flour": 7, "Spices": 4, "Quinoa": 8
    }
}

def compare_prices(grocery_list: dict) -> dict:
    result = {}

    for store, prices in PRICE_DB.items():
        total = 0

        for items in grocery_list.values():
            for item in items:
                name = item["item"]
                qty = item["quantity"]
                total += prices.get(name, 3) * qty

        result[store] = total

    best_store = min(result, key=result.get) if result else "walmart"

    return {
        "store_totals": result,
        "best_store": best_store
    }
