def remove_pantry_items(grocery_list: dict, pantry_items: list[str]) -> dict:
    """
    grocery_list: {"Grains": [{"item": "Rice", "quantity": 1}], ...}
    pantry_items: ["Rice", "Milk"]
    """
    updated_list = {}
    pantry_set = {p.lower().strip() for p in pantry_items}

    for category, items in grocery_list.items():
        filtered_items = []

        for item_obj in items:
            if item_obj["item"].lower() not in pantry_set:
                filtered_items.append(item_obj)

        if filtered_items:
            updated_list[category] = filtered_items

    return updated_list
