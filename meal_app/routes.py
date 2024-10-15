from meal_app import app
from flask import Flask, render_template, request, redirect
import json
import sqlite3
import bcrypt
import requests
import os
import re


@app.route('/')
def welcome():
    return render_template('welcome.html')

# Route to display the signup form and handle form submissions
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Hash the password before storing it
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # It should store the username and password in the database but doesn't work
        
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            return render_template('signup.html', success = True)  # Redirect after successful signup
        except sqlite3.IntegrityError:
            return render_template('signup.html', success = False)
        finally:
            conn.close()
    
    return render_template('signup.html')

# Success page
#@app.route('/success')
#def success():
#    return "Account created successfully!"

@app.route('/profile')
def profile():
    return render_template('profile.html')



recipe_search_app_id = os.getenv('RECIPE_SEARCH_APP_ID')
recipe_search_api_key = os.getenv('RECIPE_SEARCH_API_KEY')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET': 
        return render_template('search.html')
    else:
        searchbar = request.form['searchbar']
        mealtype = request.form['mealtype']
        dishtype = request.form['dishtype']
        maxIngredients = request.form['maxIngredients']
        cuisineType = request.form['cuisinetype']
        dietType = request.form['diet']
        api_url = f"https://api.edamam.com/api/recipes/v2?type=any&q={searchbar}&app_id={recipe_search_app_id}&app_key={recipe_search_api_key}&mealType={mealtype}&dishType={dishtype}&ingr={maxIngredients}&cuisineType={cuisineType}&diet={dietType}&random=false&field=uri&field=label&field=calories&field=yield&field=ingredientLines&field=source&field=images&field=url&field=totalNutrients"

        response = requests.get(api_url)

        data = response.json()

        list_of_recipes = data['hits']

        display_data = [{'label': recipe['recipe']['label'], 'calories': round(recipe['recipe']['calories']), 'servings': round(recipe['recipe']['yield']), 'cal_per_serv': round(recipe['recipe']['calories']/recipe['recipe']['yield']), 'ingredients': recipe['recipe']['ingredientLines'], 'url': recipe['recipe']['url'], 'source': recipe['recipe']['source'], 'protein': round(recipe['recipe']['totalNutrients']['PROCNT']['quantity']), 'proteinunit': recipe['recipe']['totalNutrients']['PROCNT']['unit'], 'protein_per_serv': round(recipe['recipe']['totalNutrients']['PROCNT']['quantity']/recipe['recipe']['yield'])} for recipe in list_of_recipes]
        

        return render_template('search.html', recipes=display_data, mealtype=mealtype, searchbar=searchbar, success=True)

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