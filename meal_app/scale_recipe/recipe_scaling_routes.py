from meal_app import app
from flask import Flask, render_template, request, redirect
from flask import Blueprint
import re

recipe_scaling_templates = Blueprint('recipe_scaling',__name__)

@app.route('/recipe_scaling', methods=['POST'])
def recipe_scaling():
    ingredients = request.form.getlist('ingredient')  # List of ingredient names
    adjusted_ingredients = []
    ratios = []

    # Step 1: Iterate through the ingredients, compute ratios for checked ingredients
    for index, ingredient in enumerate(ingredients, 1):
        # Check if the ingredient was selected
        if f'ingredient_selected_{index}' in request.form:
            amount_on_hand = float(request.form.get(f'amount_on_hand_{index}', 0))
            amount_needed = float(request.form.get(f'amount_needed_{index}', 0))

            if amount_on_hand > 0 and amount_needed > 0:
                ratio = amount_on_hand / amount_needed
                ratios.append(ratio)  # Collect all ratios for checked ingredients
                print(f'Ratio for {ingredient}: {ratio}')  # Debugging ratio calculation
    
    # Step 2: Find the smallest ratio from the checked ingredients
    if ratios:
        smallest_ratio = min(ratios)
        print(f'Smallest ratio: {smallest_ratio}')  # Debugging smallest ratio

        # Step 3: Scale all ingredients using the smallest ratio
        for index, ingredient in enumerate(ingredients, 1):
            amount_needed = float(request.form.get(f'amount_needed_{index}', 0))
            scaled_amount = amount_needed * smallest_ratio  # Scale using smallest ratio

            adjusted_ingredients.append({
                'name': ingredient,
                'scaledAmount': round(scaled_amount, 2)  # Rounded to 2 decimal places for display
            })

        print(f'Adjusted ingredients: {adjusted_ingredients}')  # Debugging adjusted amounts

        # Step 4: Render the scaled_recipe.html template with the adjusted ingredients
        return render_template('scaled_recipe.html', adjusted_ingredients=adjusted_ingredients)

    # If no ingredients were selected, reload the page with the same ingredients
    return render_template('recipe_scaling.html', ingredients=ingredients)