import pandas as pd

def load_recipes_from_excel(file_path):
    # Load the Excel file
    df = pd.read_excel(file_path)

    # Print column names for debugging (remove this in production)
    print("Column names in Excel file:", df.columns.tolist())

    # Initialize an empty dictionary for storing recipes
    recipes = {}

    # Iterate over each row in the DataFrame
    for _, row in df.iterrows():
        # Get the recipe title and standardize it for case-insensitive search
        recipe_name = row['title'].strip().lower()

        # Parse ingredients, amounts, and units
        ingredients = [
            {
                "name": ingredient.strip().lower(),
                "weight": amount,
                "unit": unit
            }
            for ingredient, amount, unit in zip(row['food'], row['value'], row['weight'])
        ]

        # Store each recipe in the dictionary with the recipe name as the key
        recipes[recipe_name] = {
            "recipe_name": recipe_name.title(),
            "ingredients": ingredients
        }
    
    return recipes
