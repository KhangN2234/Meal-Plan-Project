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
        return render_template('shoppingcart.html')        
    if request.method == "POST":
        print("Method called.")
        recipeURI = request.form.get('recipeURI')
        if 'user' in session:  # Check if the user is logged in
            email = session['user']
            doc_ref = db.collection('users').document(email)
        
        # Update the document to add a new field with the latest search query
            doc_ref.update({'saved_recipes': recipeURI})
            return render_template('shoppingcart.html')  