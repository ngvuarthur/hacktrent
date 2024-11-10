def calculate_adjusted_recipe(recipe, adult_portions, child_portions, dietary_restrictions):
    # Define weight per portion
    adult_weight_per_portion = 200
    child_weight_per_portion = 100
    
    # Calculate total required weight
    total_required_weight = (adult_weight_per_portion * adult_portions) + (child_weight_per_portion * child_portions)
    original_total_weight = recipe.get("original_total_weight", 0)
    adjustment_factor = total_required_weight / original_total_weight if original_total_weight else 1
    
    # Process ingredients with adjustment factor
    adjusted_ingredients = []
    for ingredient in recipe.get("ingredients", []):
        adjusted_weight = ingredient["weight"] * adjustment_factor
        adjusted_ingredients.append({
            "name": ingredient["name"],
            "weight": round(adjusted_weight, 2),
            "unit": ingredient["unit"]
        })
    
    # Check dietary restrictions
    meets_restrictions = True
    if dietary_restrictions.get("vegetarian") and "beef" in [i["name"] for i in recipe["ingredients"]]:
        meets_restrictions = False

    # Prepare result
    result = {
        "recipe_name": recipe["recipe_name"],
        "adult_portions": adult_portions,
        "child_portions": child_portions,
        "total_required_weight": total_required_weight,
        "adjustment_factor": round(adjustment_factor, 2),
        "adjusted_ingredients": adjusted_ingredients,
        "meets_restrictions": meets_restrictions
    }
    
    return result
