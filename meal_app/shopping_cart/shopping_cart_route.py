from meal_app import app, db
from flask import Flask, render_template, request, redirect, session, flash
from spellchecker import SpellChecker
import requests
import os
from flask import Blueprint
from urllib.parse import quote


recipe_search_app_id = os.getenv('RECIPE_SEARCH_APP_ID')
recipe_search_api_key = os.getenv('RECIPE_SEARCH_API_KEY')

shopping_cart_template = Blueprint('cart',__name__)

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if request.method == 'GET': 
        if 'user' in session:  # Check if the user is logged in
            email = session['user']
            doc_ref = db.collection('users').document(email)

            user_data = doc_ref.get().to_dict()
            saved_recipes = user_data.get('cart', [])
            api_url = f"https://api.edamam.com/api/recipes/v2/by-uri?type=public&app_id={recipe_search_app_id}&app_key={recipe_search_api_key}"
            for string in saved_recipes:
                encodedString = quote(string, safe='')
                api_url += "&uri=" + encodedString

                print(api_url)

                response = requests.get(api_url)

                print(response.json)

                data = response.json()

                list_of_recipes = data['hits']

                print(list_of_recipes)

                display_data = [{'label': recipe['recipe']['label'], 'uri': recipe['recipe']['uri'], 'calories': round(recipe['recipe']['calories']), 'servings': round(recipe['recipe']['yield']), 'cal_per_serv': round(recipe['recipe']['calories']/recipe['recipe']['yield']), 'ingredients': recipe['recipe']['ingredientLines'], 'url': recipe['recipe']['url'], 'source': recipe['recipe']['source'], 'protein': round(recipe['recipe']['totalNutrients']['PROCNT']['quantity']), 'proteinunit': recipe['recipe']['totalNutrients']['PROCNT']['unit'], 'protein_per_serv': round(recipe['recipe']['totalNutrients']['PROCNT']['quantity']/recipe['recipe']['yield'])} for recipe in list_of_recipes]

            return render_template('shoppingcart.html', saved_recipes=saved_recipes, recipes=display_data)
        else: return render_template('shoppingcart.html', errorMessage="Error: No user currently logged in.")
    if request.method == "POST":
        recipeURI = request.form.get('recipeURI')
        if 'user' in session:  # Check if the user is logged in
            email = session['user']
            doc_ref = db.collection('users').document(email)

            user_data = doc_ref.get().to_dict()
            saved_recipes = user_data.get('cart', [])
        
            # Update the document to add a new field with the latest search query
            if recipeURI and recipeURI not in saved_recipes:
                saved_recipes.append(recipeURI)
                doc_ref.update({'cart': saved_recipes})

                return render_template('shoppingcart.html', successMessage="Item added successfully")
            else:
                return render_template('shoppingcart.html', errorMessage="Error: Item already in cart")
            
        else:
            return render_template('shoppingcart.html', errorMessage="Error: No user currently logged in.")