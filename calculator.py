def adjust_portions(ingredients, current_portions, desired_portions):
    factor = desired_portions / current_portions
    adjusted_ingredients = []
    
    for ingredient in ingredients:
        adjusted_quantity = float(ingredient["quantity"]) * factor
        adjusted_ingredient = {
            "name": ingredient["name"],
            "quantity": round(adjusted_quantity, 2),
            "unit": ingredient["unit"]
        }
        adjusted_ingredients.append(adjusted_ingredient)
    
    return adjusted_ingredients
