STORE_LAYOUTS = {
    "walmart": [
        "Produce",
        "Dairy",
        "Protein",
        "Frozen",
        "Pantry",
        "Grains",
        "Household",
        "Other"
    ],
    "costco": [
        "Produce",
        "Dairy",
        "Protein",
        "Pantry",
        "Frozen",
        "Household",
        "Grains",
        "Other"
    ]
}

def optimize_store_route(grocery_list: dict, store: str = "walmart") -> dict:
    """
    Reorder grocery list according to store walking path
    """
    ordered = {}
    layout = STORE_LAYOUTS.get(store, STORE_LAYOUTS["walmart"])

    for category in layout:
        if category in grocery_list:
            ordered[category] = grocery_list[category]

    # Append anything not mapped
    for category in grocery_list:
        if category not in ordered:
            ordered[category] = grocery_list[category]

    return ordered
