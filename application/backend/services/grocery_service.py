from collections import defaultdict

# Map meals to ingredients (exhaustive based on meal_service.py)
MEAL_INGREDIENT_MAP = {
    "Oats with fruits": ["Oats", "Milk", "Banana"],
    "Smoothie": ["Milk", "Banana", "Oats"],
    "Upma": ["Semolina", "Vegetables"],
    "Brown rice + dal + salad": ["Brown Rice", "Dal", "Tomato", "Cucumber", "Lettuce"],
    "Quinoa bowl": ["Quinoa", "Vegetables", "Olive Oil"],
    "Roti + vegetables": ["Wheat flour", "Vegetables"],
    "Soup + salad": ["Vegetables", "Spices", "Tomato", "Cucumber"],
    
    "Paneer sandwich": ["Bread", "Paneer", "Vegetables"],
    "Protein smoothie": ["Milk", "Banana", "Protein Powder"],
    "Rice + dal + paneer": ["Rice", "Dal", "Paneer"],
    "Roti + paneer curry": ["Wheat flour", "Paneer", "Spices", "Tomato"],
    
    "Poha": ["Rice Flakes", "Peanuts", "Spices"],
    "Idli": ["Rice", "Dal"],
    "Rice + dal + sabzi": ["Rice", "Dal", "Vegetables"],
    "Roti + curry": ["Wheat flour", "Vegetables", "Spices"],
    
    "Egg whites + toast": ["Eggs", "Bread"],
    "Grilled chicken + salad": ["Chicken Breast", "Tomato", "Cucumber", "Lettuce", "Olive Oil"],
    "Chicken soup": ["Chicken Breast", "Vegetables", "Spices"],
    
    "Eggs + toast": ["Eggs", "Bread"],
    "Chicken breast + rice + broccoli": ["Chicken Breast", "Rice", "Broccoli"],
    "Beef steak + sweet potato": ["Beef Steak", "Sweet Potato", "Olive Oil"],
    
    "Omelette": ["Eggs", "Vegetables", "Olive Oil"],
    "Chicken curry + rice": ["Chicken Breast", "Rice", "Spices", "Tomato"],
    "Fish + vegetables": ["Fish", "Vegetables", "Olive Oil"],
    
    "Oats": ["Oats", "Milk"],
    "Salad": ["Tomato", "Cucumber", "Vegetables"],
    "Soup": ["Vegetables", "Spices"],
    "Rice + dal": ["Rice", "Dal"]
}

# Category mapping
CATEGORY_MAP = {
    "Oats": "Grains",
    "Rice": "Grains",
    "Brown Rice": "Grains",
    "Wheat flour": "Grains",
    "Quinoa": "Grains",
    "Semolina": "Grains",
    "Bread": "Grains",
    "Rice Flakes": "Grains",
    
    "Milk": "Dairy",
    "Paneer": "Dairy",
    
    "Dal": "Protein",
    "Eggs": "Protein",
    "Chicken Breast": "Protein",
    "Beef Steak": "Protein",
    "Fish": "Protein",
    "Protein Powder": "Protein",
    
    "Banana": "Produce",
    "Tomato": "Produce",
    "Cucumber": "Produce",
    "Vegetables": "Produce",
    "Lettuce": "Produce",
    "Broccoli": "Produce",
    "Sweet Potato": "Produce",
    
    "Spices": "Pantry",
    "Olive Oil": "Pantry",
    "Peanuts": "Pantry"
}

def generate_grocery_list(meal_plan: dict) -> dict:
    grocery = defaultdict(int)

    for day, meals in meal_plan.items():
        # Handle both single format (meals: {breakfast, lunch, dinner}) and family format (meals.breakfast...)
        meals_dict = meals.get("meals", meals) 
        
        for meal_type in ["breakfast", "lunch", "dinner"]:
            meal_item = meals_dict.get(meal_type, "")
            meal_name = meal_item.get("name", "") if isinstance(meal_item, dict) else meal_item
            ingredients = MEAL_INGREDIENT_MAP.get(meal_name, [])
            # Fallback if unknown meal
            if not ingredients and meal_name:
                ingredients = [meal_name]

            for item in ingredients:
                grocery[item] += 1

    # Categorize
    categorized = defaultdict(list)

    for item, qty in grocery.items():
        category = CATEGORY_MAP.get(item, "Other")
        categorized[category].append({
            "item": item,
            "quantity": qty
        })

    return dict(categorized)
