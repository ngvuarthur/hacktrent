import pandas as pd

def load_recipes_from_excel(file_path):
    recipes = {}
    df = pd.read_excel(file_path)

    for _, row in df.iterrows():
        recipe_name = row['Recipe Name'].strip().lower()
        ingredients = [
            {"name": ingredient.strip().lower(), "weight": weight, "unit": unit}
            for ingredient, weight, unit in zip(
                row['Ingredients'].split(','), row['Weights'].split(','), row['Units'].split(',')
            )
        ]
        recipes[recipe_name] = {
            "recipe_name": recipe_name.title(),
            "original_total_weight": row['Total Weight'],
            "ingredients": ingredients
        }
    
    return recipes

def search_recipe_online(name, recipes):
    # Convert the recipe name to lowercase for case-insensitive lookup
    name = name.strip().lower()
    return recipes.get(name, None)
