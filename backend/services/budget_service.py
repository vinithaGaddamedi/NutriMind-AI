ITEM_PRICE_MAP = {
    "Rice": 5,
    "Dal": 4,
    "Milk": 3,
    "Banana": 2,
    "Vegetables": 6,
    "Oats": 4,
    "Wheat flour": 5,
    "Tomato": 3,
    "Cucumber": 2,
    "Spices": 5,
    "Quinoa": 7
}

def calculate_total(grocery_list: dict) -> float:
    total = 0
    for items in grocery_list.values():
        for item_obj in items:
            price = ITEM_PRICE_MAP.get(item_obj["item"], 3) # default $3
            total += price * item_obj["quantity"]
    return total

def optimize_for_budget(grocery_list: dict, budget: float):
    total = calculate_total(grocery_list)

    if total <= budget:
        return grocery_list, total, "Within budget"

    # Simple optimization: reduce quantity of items or remove them
    reduced_list = {}

    for category, items in grocery_list.items():
        reduced_list[category] = []
        for item_obj in items:
            # Drop item if it's the last one in category as a naive optimization, or reduce qty
            new_qty = max(1, item_obj["quantity"] - 1)
            # Actually, the prompt says `items[:-1]`
            # Let's use the prompt's naive logic: remove last item in category if multiple exist
            pass
        
        # Prompt's logic:
        if len(items) > 1:
            reduced_list[category] = items[:-1]
        else:
            reduced_list[category] = items

    new_total = calculate_total(reduced_list)
    
    # If still over, just return as is but modified
    status = "Adjusted to fit budget" if new_total <= budget else "Adjusted, but still slightly over budget"

    return reduced_list, new_total, status
