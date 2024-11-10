from flask import Flask, request, jsonify, render_template
import pandas as pd
from calculator import calculate_adjusted_recipe, adjust_ingredient_units
import ast

# Initialize the Flask app
app = Flask(_name_)

# Load the recipe and restriction datasets
recipe_df = pd.read_excel('recipedatabase.xlsx')
restriction_df = pd.read_excel('foodrestrictiondatabase.xlsx')
# Load the conversion table
conversion_df = pd.read_excel('unitconversiondata.xlsx')

def check_restriction(recipe_name, restriction):
    """
    Check if the recipe contains any ingredients that conflict with the given dietary restriction.
    """
    recipe_row = recipe_df[recipe_df['title'].str.lower() == recipe_name.lower()]
    
    if recipe_row.empty:
        return None  # Recipe not found
    
    recipe_ingredients = [ingredient.strip().lower() for ingredient in ast.literal_eval(recipe_row.iloc[0]['food'].replace('\u00A0', ' '))]
    
    if restriction not in restriction_df.columns:
        return f"No {restriction} restriction in the {recipe_name} recipe"

    restricted_items_str = restriction_df[restriction].dropna().iloc[0]
    restricted_items = [item.strip().lower() for item in ast.literal_eval(restricted_items_str)]
    
    for ingredient in recipe_ingredients:
        for restricted_item in restricted_items:
            if ingredient == restricted_item or restricted_item in ingredient or ingredient in restricted_item:
                return f"{recipe_name} is non-{restriction}: contains {ingredient}"
    
    return f"No {restriction} restriction in the {recipe_name} recipe"

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/optimize_recipe", methods=["POST"])
def optimize_recipe():
    data = request.json
    recipe_name = data.get("recipe_name", "").strip().lower()
    adult_portions = int(data.get("adult_portions", 0))
    child_portions = int(data.get("child_portions", 0))
    dietary_restrictions = data.get("dietary_restrictions", {})

    selected_restriction = None
    for restriction, is_selected in dietary_restrictions.items():
        if is_selected:
            selected_restriction = restriction
            break

    restriction_message = None

    # Case when "none" restriction is selected
    if selected_restriction == "none":
        recipe_row = recipe_df[recipe_df['title'].str.lower() == recipe_name]
        if not recipe_row.empty:
            result = calculate_adjusted_recipe(recipe_row.iloc[0], adult_portions=adult_portions, child_portions=child_portions)
            
            # Adjust units in the ingredient list here
            result = adjust_ingredient_units(result)

            result_html = f"<h2>Ingredient list for {adult_portions} adult portions and {child_portions} child portions:</h2><ul>"
            for ingredient in result:
                result_html += f"<li>{ingredient}</li>"
            result_html += "</ul>"

            # Display recipe steps from the 'recipe' column
            if 'recipe' in recipe_row.columns:
                recipe_steps = eval(recipe_row.iloc[0]['recipe'])  # Convert the string to a list
                result_html += f"<h2>{recipe_name.title()} Recipe:</h2><ul>"
                for step in recipe_steps:
                    result_html += f"<li>{step}</li>"
                result_html += "</ul>"
            else:
                result_html += "<p>No recipe steps available for this dish.</p>"

            return jsonify({"html": result_html})
        else:
            return jsonify({"html": "<p>Recipe not found.</p>"}), 404

    # Case when a specific restriction is selected
    if selected_restriction and selected_restriction != "none":
        restriction_message = check_restriction(recipe_name, selected_restriction)
        if "non-" in restriction_message:
            return jsonify({"html": f"<p>{restriction_message}</p>"})
        else:
            recipe_row = recipe_df[recipe_df['title'].str.lower() == recipe_name]
            if not recipe_row.empty:
                result = calculate_adjusted_recipe(recipe_row.iloc[0], adult_portions=adult_portions, child_portions=child_portions)
                
                # Adjust units in the ingredient list here
                result = adjust_ingredient_units(result)

                result_html = f"<p>{restriction_message}</p><h2>Ingredient list for {adult_portions} adult portions and {child_portions} child portions:</h2><ul>"
                for ingredient in result:
                    result_html += f"<li>{ingredient}</li>"
                result_html += "</ul>"

                # Display recipe steps from the 'recipe' column
                if 'recipe' in recipe_row.columns:
                    recipe_steps = eval(recipe_row.iloc[0]['recipe'])  # Convert the string to a list
                    result_html += f"<h2>{recipe_name.title()} Recipe:</h2><ul>"
                    for step in recipe_steps:
                        result_html += f"<li>{step}</li>"
                    result_html += "</ul>"
                else:
                    result_html += "<p>No recipe steps available for this dish.</p>"

                return jsonify({"html": result_html})
            else:
                return jsonify({"html": "<p>Recipe not found.</p>"}), 404