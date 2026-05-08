from datetime import datetime

def get_expiring_items(pantry: list) -> list:
    today = datetime.today()
    expiring = []

    for item in pantry:
        if "expiry_date" not in item:
            continue
        try:
            expiry = datetime.strptime(item["expiry_date"], "%Y-%m-%d")
            days_left = (expiry - today).days

            if 0 <= days_left <= 3:
                expiring.append(item["item"])
        except ValueError:
            pass

    return expiring

def generate_alerts(pantry_history: list) -> list:
    today = datetime.today()
    alerts = []

    for item in pantry_history:
        if "last_used" not in item:
            continue
        try:
            last_used = datetime.strptime(item["last_used"], "%Y-%m-%d")
            days_unused = (today - last_used).days

            if days_unused > 5:
                alerts.append(f"You haven’t used {item['item']} in {days_unused} days. Try incorporating it into your next meal!")
        except ValueError:
            pass

    return alerts

def score_meal_with_expiry(meal: str, pantry_items: list, expiring_items: list) -> int:
    """
    Boost score if item is expiring
    """
    # Simple mock ingredient mapping
    ingredient_mock = meal.lower().split(" ")
    score = 0

    for item in ingredient_mock:
        clean_item = item.strip("+,.")
        if any(clean_item in p.lower() for p in pantry_items):
            score += 1
        if any(clean_item in e.lower() for e in expiring_items):
            score += 2  # priority boost

    return score
