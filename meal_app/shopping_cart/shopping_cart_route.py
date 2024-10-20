from meal_app import app
from flask import Flask, render_template, request, redirect
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
