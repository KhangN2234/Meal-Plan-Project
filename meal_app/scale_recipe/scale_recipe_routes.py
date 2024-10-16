from meal_app import app
from flask import Flask, render_template, request, redirect
from flask import Blueprint
import re

scaled_recipe_templates = Blueprint('scaled_recipe',__name__)

@app.route('/scale_recipe', methods=['POST'])
def scale_recipe():
    # Get the list of ingredients from the POST request
    ingredients = request.form.getlist('ingredients[]')
    processed_ingredients = []

    # Regular expression pattern to capture the optional amount and the rest of the string
    pattern = r'(\d*\.?\d+)?\s*(.*)'

    for ingredient in ingredients:
        match = re.match(pattern, ingredient)

        if match:
            # Extract the amount (if it exists) or default to 0
            amount_needed = float(match.group(1)) if match.group(1) else 0
            ingredient_name = match.group(2).strip()  # Extract the rest of the string as the ingredient name
            
            # Append the processed ingredient (as a dictionary) to the list
            processed_ingredients.append({
                'amount_needed': amount_needed,
                'ingredient': ingredient_name,
                'amount_on_hand': 0
            })

    # Pass the ingredient list to the recipe scaling template
    return render_template('recipe_scaling.html', ingredients=processed_ingredients)