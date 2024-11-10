from flask import Flask, render_template, request, jsonify
from services import load_recipes_from_excel, search_recipe_online
from calculator import calculate_adjusted_recipe

app = Flask(__name__)

# Load recipes from the Excel file once when the app starts
recipes = None

def load_recipes():
    global recipes
    # Use the absolute path to the Excel file
    recipes = load_recipes_from_excel(r"C:\Users\DELL\Downloads\recipedatabase.xlsx")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/optimize_recipe', methods=['POST'])
def optimize_recipe():
    try:
        data = request.get_json()
        recipe_name = data.get("recipe_name")
        adult_portions = int(data.get("adult_portions", 1))
        child_portions = int(data.get("child_portions", 0))
        dietary_restrictions = data.get("dietary_restrictions", {})

        # Fetch the recipe from the loaded recipes dictionary
        recipe_data = search_recipe_online(recipe_name, recipes)
        
        if recipe_data is None:
            return jsonify({"error": "Recipe not found"}), 404

        # Calculate the adjusted recipe based on portions and dietary restrictions
        adjusted_recipe = calculate_adjusted_recipe(recipe_data, adult_portions, child_portions, dietary_restrictions)
        
        # Format the response to be displayed on the webpage
        html_response = f"""
        <h2>Adjusted Recipe: {adjusted_recipe['recipe_name']}</h2>
        <p>Adult Portions: {adjusted_recipe['adult_portions']}</p>
        <p>Child Portions: {adjusted_recipe['child_portions']}</p>
        <p>Total Required Weight: {adjusted_recipe['total_required_weight']} grams</p>
        <p>Adjustment Factor: {adjusted_recipe['adjustment_factor']}</p>
        <h3>Adjusted Ingredients:</h3>
        <ul>
        """
        for ingredient in adjusted_recipe["adjusted_ingredients"]:
            html_response += f"<li>{ingredient['name']}: {ingredient['weight']} {ingredient['unit']}</li>"
        html_response += "</ul>"
        
        # Add dietary restriction information
        if adjusted_recipe["meets_restrictions"]:
            html_response += "<p>This recipe meets your dietary restrictions.</p>"
        else:
            html_response += "<p><strong>Warning:</strong> This recipe does not meet your dietary restrictions.</p>"

        return jsonify({"html": html_response})
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

# Load recipes when the app starts
load_recipes()
