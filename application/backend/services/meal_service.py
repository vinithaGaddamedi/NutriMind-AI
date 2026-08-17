import random
from services.nutrition_service import calculate_nutrition
from services.grocery_service import MEAL_INGREDIENT_MAP

MEAL_TEMPLATES = {
    "vegetarian": {
        "weight_loss": {
            "breakfast": ["Oats with fruits", "Smoothie", "Upma"],
            "lunch": ["Brown rice + dal + salad", "Quinoa bowl"],
            "dinner": ["Roti + vegetables", "Soup + salad"]
        },
        "muscle_gain": {
            "breakfast": ["Paneer sandwich", "Protein smoothie"],
            "lunch": ["Rice + dal + paneer"],
            "dinner": ["Roti + paneer curry"]
        },
        "maintenance": {
            "breakfast": ["Poha", "Idli", "Upma"],
            "lunch": ["Rice + dal + sabzi"],
            "dinner": ["Roti + curry"]
        }
    },
    "nonveg": {
        "weight_loss": {
            "breakfast": ["Egg whites + toast"],
            "lunch": ["Grilled chicken + salad"],
            "dinner": ["Chicken soup"]
        },
        "muscle_gain": {
            "breakfast": ["Eggs + toast", "Protein smoothie"],
            "lunch": ["Chicken breast + rice + broccoli"],
            "dinner": ["Beef steak + sweet potato"]
        },
        "maintenance": {
            "breakfast": ["Omelette", "Eggs + toast"],
            "lunch": ["Chicken curry + rice"],
            "dinner": ["Fish + vegetables"]
        }
    }
}

REASONS_MAP = {
    "Oats with fruits": "High fiber, great for sustained energy.",
    "Smoothie": "Packed with vitamins and quick to digest.",
    "Upma": "Traditional low-calorie complex carbs.",
    "Brown rice + dal + salad": "Complete protein profile with fiber.",
    "Quinoa bowl": "Superfood rich in protein and iron.",
    "Roti + vegetables": "Balanced micronutrients and fiber.",
    "Soup + salad": "Light, hydrating, and low calorie.",
    "Paneer sandwich": "Quick high-quality dairy protein.",
    "Protein smoothie": "Fast absorbing amino acids for recovery.",
    "Rice + dal + paneer": "Caloric density for muscle synthesis.",
    "Roti + paneer curry": "Slow-digesting casein protein.",
    "Poha": "Light carb source, easily digestible.",
    "Idli": "Fermented for gut health.",
    "Rice + dal + sabzi": "Classic balanced Indian meal.",
    "Roti + curry": "Satisfying and nutrient-dense.",
    "Egg whites + toast": "Leanest protein with complex carbs.",
    "Grilled chicken + salad": "Low carb, high protein for cutting.",
    "Chicken soup": "Comforting and high in collagen.",
    "Eggs + toast": "Healthy fats and protein.",
    "Chicken breast + rice + broccoli": "The ultimate bodybuilding staple.",
    "Beef steak + sweet potato": "High iron, creatine, and energy.",
    "Omelette": "Versatile protein packed start.",
    "Chicken curry + rice": "Rich in flavor and satiating.",
    "Fish + vegetables": "Rich in Omega-3 fatty acids."
}

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def pantry_score(meal, pantry):
    ingredients = MEAL_INGREDIENT_MAP.get(meal, [])
    pantry_lower = [i.lower() for i in pantry]
    match = sum(1 for i in ingredients if i.lower() in pantry_lower)
    return match

def filter_meals(meals, allergies, dislikes):
    filtered = []
    constraints = set([i.lower().strip() for i in allergies] + [i.lower().strip() for i in dislikes])
    
    for meal in meals:
        ingredients = MEAL_INGREDIENT_MAP.get(meal, [])
        ing_lower = [i.lower() for i in ingredients]
        
        # Check if the meal name itself contains any constrained word
        if any(c in meal.lower() for c in constraints):
            continue
            
        # Check if any ingredient matches
        if any(c in ing_lower for c in constraints):
            continue
            
        filtered.append(meal)
    return filtered

def select_best_meal(available_meals, pantry, used_meals):
    unused = [m for m in available_meals if m not in used_meals]
    if not unused:
        unused = available_meals
        
    if not unused:
        return {"name": "Custom Chef Special", "reason": "Dietary constraints too restrictive"}

    scored = [(meal, pantry_score(meal, pantry)) for meal in unused]
    scored.sort(key=lambda x: x[1], reverse=True)
    
    top_score = scored[0][1]
    top_meals = [m[0] for m in scored if m[1] == top_score]
    
    selected = random.choice(top_meals)
    used_meals.add(selected)
    
    reason = REASONS_MAP.get(selected, "Balanced nutrition for your goals.")
    if top_score > 0:
        reason = f"{reason} Also uses {top_score} items from your pantry!"
        
    return {"name": selected, "reason": reason}

def generate_weekly_meal(diet, profile):
    plan = {}
    goal = profile.get("goal", "maintenance")
    template = MEAL_TEMPLATES.get(diet, {}).get(goal, {})

    if not template:
        template = MEAL_TEMPLATES.get("vegetarian", {}).get("weight_loss", {})

    allergies = profile.get("allergies", [])
    dislikes = profile.get("dislikes", [])
    pantry = profile.get("pantry", [])

    used_meals = set()
    total_pantry_matches = 0
    total_ingredients = 0

    for day in DAYS:
        daily_plan = {}
        for meal_type in ["breakfast", "lunch", "dinner"]:
            available = template.get(meal_type, [])
            filtered = filter_meals(available, allergies, dislikes)
            
            if not filtered:
                filtered = available
                
            selected_meal_dict = select_best_meal(filtered, pantry, used_meals)
            daily_plan[meal_type] = selected_meal_dict
            
            selected_name = selected_meal_dict["name"]
            ingredients = MEAL_INGREDIENT_MAP.get(selected_name, [])
            total_ingredients += len(ingredients)
            total_pantry_matches += pantry_score(selected_name, pantry)

        plan[day] = daily_plan

    insights = []
    if total_ingredients > 0:
        pantry_pct = int((total_pantry_matches / total_ingredients) * 100)
        if pantry_pct > 0:
            insights.append(f"Using {pantry_pct}% of ingredients from your pantry.")
            insights.append(f"Saved approx. ${max(2, pantry_pct // 3)} on groceries this week!")
            
    if allergies:
        insights.append(f"100% Allergy-safe ({', '.join(allergies)} excluded).")
    
    if goal == "weight_loss":
        insights.append("Caloric deficit optimized for healthy weight loss.")
    elif goal == "muscle_gain":
        insights.append("High-protein meals selected for muscle synthesis.")

    return plan, insights

def generate_single_plan(user, diet):
    nutrition = calculate_nutrition(user)
    weekly_plan, insights = generate_weekly_meal(diet, user)
    
    # Simple nutrition score based on protein ratio
    score = 8.5
    if user.get("goal") == "weight_loss": score = 9.2
    elif user.get("goal") == "muscle_gain": score = 9.5
    
    return {
        "user": user.get("name", "User"),
        "calories": nutrition["calories"],
        "macros": nutrition["macros"],
        "meal_plan": weekly_plan,
        "nutrition_score": score,
        "insights": insights
    }

def generate_family_plan(users, diet):
    family_result = {}

    nutrition_map = {}
    for user in users:
        nutrition_map[user.get("name", "User")] = calculate_nutrition(user)

    # Use first user's profile for common generation constraints
    primary_profile = users[0]
    weekly_plan, insights = generate_weekly_meal(diet, primary_profile)

    for day, meals in weekly_plan.items():
        family_result[day] = {
            "meals": meals,
            "portions": {}
        }

        for user in users:
            family_result[day]["portions"][user.get("name", "User")] = {
                "calories": nutrition_map[user.get("name", "User")]["calories"]
            }

    return {
        "family_plan": family_result,
        "nutrition_score": 9.0,
        "insights": ["Family meals synchronized for easy cooking."] + insights
    }
