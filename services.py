import pandas as pd

def load_recipes_from_excel(file_path):
    recipes = {}
    df = pd.read_excel(file_path)

    for _, row in df.iterrows():
        recipe_name = row['title'].strip().lower()
        ingredients = [
            {"name": ingredient.strip().lower(), "weight": weight, "unit": unit}
            for ingredient, weight, unit in zip(
                row['ingredients'].split(','), row['weight'].split(','), row['food'].split(',')

            )
        ]
        recipes[recipe_name] = {
            "recipe_name": recipe_name.title(),
            "original_total_weight": row['total recipe weight(g)'],
            "ingredients": ingredients
        }
    
    return recipes

def search_recipe_online(name, recipes):
    # Convert the recipe name to lowercase for case-insensitive lookup
    name = name.strip().lower()
    return recipes.get(name, None)