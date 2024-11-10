import pandas as pd

# Load the conversion table
conversion_df = pd.read_excel('unitconversiondata.xlsx')

def calculate_adjusted_recipe(recipe, adult_portions, child_portions):
    # Retrieve portion weights from the recipe dictionary
    adult_weight_per_portion = recipe.get("adult portion size(g)", 0)
    child_weight_per_portion = recipe.get("child portion size(g)", 0)
    total_recipe_weight = recipe.get("total recipe weight(g)", 1)
    
    # Calculate total required weight
    total_required_weight = (adult_weight_per_portion * adult_portions) + (child_weight_per_portion * child_portions)
    
    # Calculate adjustment factor and keep to 3 decimal places
    adjustment_factor = round(total_required_weight / total_recipe_weight, 3)
    
    # Clean non-printable characters
    value_cleaned = recipe["value"].replace('\u00A0', ' ')
    weight_cleaned = recipe["weight"].replace('\u00A0', ' ')
    food_cleaned = recipe["food"].replace('\u00A0', ' ')
    
    # Adjust ingredients based on the adjustment factor
    adjusted_ingredients = []
    for qty, unit, food_name in zip(eval(value_cleaned), eval(weight_cleaned), eval(food_cleaned)):
        # Calculate adjusted quantity
        adjusted_qty = qty * adjustment_factor if qty != 0 else 0
        
        # Apply custom rounding rules
        if adjusted_qty < 1:
            adjusted_qty = round(adjusted_qty, 3)  # Allow three decimal places if below 1
        else:
            # Get second decimal place
            second_decimal = int((adjusted_qty * 100) % 10)
            if second_decimal >= 3:
                adjusted_qty = round(adjusted_qty, 1)  # One decimal place if second decimal >= 3
            else:
                adjusted_qty = round(adjusted_qty)  # Round to whole number if second decimal <= 2

        # Format ingredient line based on unit
        if qty == 0 and unit == "0":
            # If both value and weight are 0, just print the food name
            adjusted_ingredients.append(f"{food_name}".strip())
        elif qty == 0:
            # If value is 0 but weight is present, print weight and food name
            adjusted_ingredients.append(f"{unit} {food_name}".strip())
        elif unit == "0":
            # If unit is 0, print only the adjusted quantity and food name
            adjusted_ingredients.append(f"{adjusted_qty} {food_name}".strip())
        else:
            # Print adjusted quantity, unit, and food name
            adjusted_ingredients.append(f"{adjusted_qty} {unit} {food_name}".strip())
    
    # Return the adjusted ingredients list
    return adjusted_ingredients


def convert_unit(quantity, unit):
    for _, row in conversion_df.iterrows():
        if row['fromUnit'] == unit:
            # Apply conversion factor
            quantity *= row['conversionFactor']
            unit = row['toUnit']
            
            # Specific handling for large and small units based on kitchen use cases
            if unit == 'g' and quantity >= 1000:
                quantity /= 1000
                unit = 'kg'
            elif unit == 'kg' and quantity < 1:
                quantity *= 1000
                unit = 'g'
                
            elif unit == 'ml' and quantity >= 1000:
                quantity /= 1000
                unit = 'L'
            elif unit == 'L' and quantity < 1:
                quantity *= 1000
                unit = 'ml'
                
            elif unit == 'tsp' and quantity >= 3:
                quantity /= 3
                unit = 'tbsp'
                
            elif unit == 'tbsp' and quantity >= 16:
                quantity /= 16
                unit = 'cup'
                
            # Only convert cups to liters for extremely large quantities (over 500 cups)
            elif unit == 'cup' and quantity >= 500:
                quantity /= 4.22675
                unit = 'L'
            elif unit == 'L' and quantity < 0.236588:
                quantity *= 4.22675
                unit = 'cup'
                
            elif unit == 'oz' and quantity >= 16:
                quantity /= 16
                unit = 'lb'
            elif unit == 'lb' and quantity < 1:
                quantity *= 16
                unit = 'oz'

    return round(quantity, 2), unit



def adjust_ingredient_units(ingredient_list):
    """
    Adjust the units of ingredients in the list based on predefined thresholds.
    Uses the convert_unit function to manage conversions.
    """
    adjusted_ingredients = []
    for ingredient in ingredient_list:
        # Split the ingredient into parts
        parts = ingredient.split()
        
        # Check if the first part is a quantity (numeric) or directly a food name (e.g., "Salt")
        try:
            quantity = float(parts[0])  # Try converting the first part to float
            unit = parts[1] if len(parts) > 1 else ""
            food_name = " ".join(parts[2:]) if len(parts) > 2 else ""
            
            # Convert units if needed
            new_quantity, new_unit = convert_unit(quantity, unit)
            
            # Add the converted ingredient to the list
            adjusted_ingredients.append(f"{new_quantity} {new_unit} {food_name}".strip())
        except ValueError:
            # If the first part is not a number, treat it as a food name without quantity/unit
            adjusted_ingredients.append(ingredient)  # Directly add ingredient as it is

    return adjusted_ingredients