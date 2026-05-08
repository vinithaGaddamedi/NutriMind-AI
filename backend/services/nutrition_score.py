HEALTH_SCORE_MAP = {
    "Oats with fruits": 9,
    "Smoothie": 8,
    "Avocado toast": 7,
    "Brown rice + dal + salad": 9,
    "Quinoa bowl": 10,
    "Chicken salad": 8,
    "Roti + vegetables": 8,
    "Soup + salad": 9,
    "Grilled salmon + veggies": 10,
    "Rice": 6,
    "Fried food": 3,
    "Dal": 8,
    "Mixed vegetables": 9
}

def calculate_meal_score(meal_plan: dict) -> float:
    total_score = 0
    count = 0

    # Handle both single and family plan formats
    if "Monday" in meal_plan and "breakfast" in meal_plan["Monday"]:
        # Single format
        for day, meals in meal_plan.items():
            for meal_item in meals.values():
                meal_name = meal_item["name"] if isinstance(meal_item, dict) else meal_item
                score = HEALTH_SCORE_MAP.get(meal_name, 7) # Default score
                total_score += score
                count += 1
    else:
        # Family format has {"meals": {"breakfast": ...}}
        for day, plan in meal_plan.items():
            for meal_item in plan["meals"].values():
                meal_name = meal_item["name"] if isinstance(meal_item, dict) else meal_item
                score = HEALTH_SCORE_MAP.get(meal_name, 7)
                total_score += score
                count += 1

    return round(total_score / count, 1) if count else 0
