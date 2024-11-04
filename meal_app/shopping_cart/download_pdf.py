from meal_app import app, db
from flask import Flask, render_template, request, redirect, session, flash
from spellchecker import SpellChecker
import requests
import os
from flask import Blueprint

recipe_search_app_id = os.getenv('RECIPE_SEARCH_APP_ID')
recipe_search_api_key = os.getenv('RECIPE_SEARCH_API_KEY')


@app.route('/download_pdf', methods=['POST'])
def download_pdf():
    if 'user' in session:  # Check if the user is logged in
        email = session['user']
        doc_ref = db.collection('users').document(email)
        user_data = doc_ref.get().to_dict()
        saved_recipes = user_data.get('cart', [])
        
        all_ingredients = []

        for recipe_uri in saved_recipes:
            # Call the API for each URI to get recipe details (if needed)
            encoded_string = quote(recipe_uri, safe='')
            api_url = f"https://api.edamam.com/api/recipes/v2/by-uri?type=public&app_id={recipe_search_app_id}&app_key={recipe_search_api_key}&uri={encoded_string}"
            response = requests.get(api_url)
            data = response.json()
            list_of_recipes = data.get('hits', [])

            for recipe in list_of_recipes:
                recipe_label = recipe['recipe']['label']
                for item in recipe['recipe']['ingredients']:
                    measure = item.get('measure', "")
                    if measure == "<unit>":
                        measure = "​"
                    processed_item = {
                        'quantity': round(item.get('quantity', 0), 2),
                        'measure': measure,
                        'food': item.get('food', "Unknown"),
                        'recipe': recipe_label
                    }
                    all_ingredients.append(processed_item)