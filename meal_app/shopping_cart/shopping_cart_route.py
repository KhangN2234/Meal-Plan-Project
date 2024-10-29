from meal_app import app, db
from flask import Flask, render_template, request, redirect, session, flash
from spellchecker import SpellChecker
import requests
import os
from flask import Blueprint


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
        return render_template('shoppingcart.html', saved_recipes=saved_recipes)
           
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