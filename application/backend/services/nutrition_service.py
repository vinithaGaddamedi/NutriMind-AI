def calculate_bmr(weight, height, age, gender="male"):
    """
    Mifflin-St Jeor Equation
    weight: kg
    height: cm
    age: years
    """
    if gender == "male":
        return 10 * weight + 6.25 * height - 5 * age + 5
    else:
        return 10 * weight + 6.25 * height - 5 * age - 161


def adjust_calories(bmr, goal):
    if goal == "weight_loss":
        return bmr - 500
    elif goal == "muscle_gain":
        return bmr + 300
    return bmr


def calculate_macros(calories):
    """
    Split:
    Protein: 30%
    Carbs: 40%
    Fats: 30%
    """
    protein = (calories * 0.3) / 4
    carbs = (calories * 0.4) / 4
    fats = (calories * 0.3) / 9

    return {
        "protein_g": round(protein),
        "carbs_g": round(carbs),
        "fats_g": round(fats),
        "iron_mg": round(calories * 0.008, 1),
        "calcium_mg": round(calories * 0.4, 1),
        "vitamin_a_iu": round(calories * 1.5, 1)
    }


def calculate_nutrition(user):
    bmr = calculate_bmr(
        user["weight"],
        user["height"],
        user["age"],
        user.get("gender", "male")
    )

    calories = adjust_calories(bmr, user["goal"])
    macros = calculate_macros(calories)

    return {
        "calories": int(calories),
        "macros": macros
    }
