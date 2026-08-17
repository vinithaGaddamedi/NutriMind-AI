import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../backend')))
from services.grocery_service import generate_grocery_list

def test_meal_to_grocery_flow():
    # Mocking meal plan payload 
    meal_plan = {
        "Monday": {
            "breakfast": "Oats with fruits",
            "lunch": "Brown rice + dal + salad"
        }
    }
    
    # Integrating with the actual grocery generation backend service
    grocery = generate_grocery_list(meal_plan)
    
    assert grocery is not None
    assert "Oats" in grocery.get("Grains", []) or any("Oats" in item["item"] for items in grocery.values() for item in items)
