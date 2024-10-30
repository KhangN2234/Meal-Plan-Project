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
        return renderCart("","")
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

                return renderCart(successMessage="Item added successfully", errorMessage="")
            else:
                return renderCart(successMessage="", errorMessage="Error: Item already in cart")
            
        else:
            return render_template('shoppingcart.html', errorMessage="Error: No user currently logged in.")
        
def renderCart(successMessage, errorMessage):
    if 'user' in session:  # Check if the user is logged in
        email = session['user']
        doc_ref = db.collection('users').document(email)

        user_data = doc_ref.get().to_dict()
        saved_recipes = user_data.get('cart', [])
        api_url = f"https://api.edamam.com/api/recipes/v2/by-uri?type=public&app_id={recipe_search_app_id}&app_key={recipe_search_api_key}"
        for string in saved_recipes:
            encodedString = quote(string, safe='')
            api_url += "&uri=" + encodedString

            response = requests.get(api_url)

            data = response.json()

            list_of_recipes = data['hits']

            result = []

            for recipe in list_of_recipes:
                for item in recipe['recipe']['ingredients']:
                    processed_item = {
                        'quantity': item.get('quantity'),
                        'measure': item.get('measure'),
                        'food': item.get('food'),
                        "recipe": recipe['recipe']['label']
                    }
                    result.append(processed_item)

        return render_template('shoppingcart.html', saved_recipes=saved_recipes, recipes=display_data, result=result, successMessage=successMessage, errorMessage=errorMessage)
    else: return render_template('shoppingcart.html', errorMessage="Error: No user currently logged in.")