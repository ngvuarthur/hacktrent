from flask import Flask, request, jsonify
from app.models import Recipe
from app.services import search_recipe_online, get_environmental_impact_score
from app.calculator import adjust_portions

app = Flask(__name__)

@app.route('/optimize_recipe', methods=['POST'])
def optimize_recipe():
    data = request.json
    recipe_name = data.get("recipe_name")
    adult_portions = data.get("adult_portions", 1)
    child_portions = data.get("child_portions", 0)
    exclude_ingredients = data.get("exclude_ingredients", [])

    # Fetch the recipe
    recipe_data = search_recipe_online(recipe_name)
    
    # Adjust portions
    total_portions = adult_portions + (child_portions * 0.5)
    adjusted_ingredients = adjust_portions(recipe_data["ingredients"], current_portions=1, desired_portions=total_portions)

    # Filter out excluded ingredients
    adjusted_ingredients = [i for i in adjusted_ingredients if i["name"] not in exclude_ingredients]
    
    # Get environmental impact score
    environmental_impact = get_environmental_impact_score(adjusted_ingredients)
    
    # Create recipe object
    recipe = Recipe(
        name=recipe_data["name"],
        ingredients=adjusted_ingredients,
        instructions=recipe_data["instructions"],
        dietary_restrictions=recipe_data["dietary_restrictions"]
    )
    recipe.environmental_impact_score = environmental_impact

    return jsonify(recipe.to_dict())
