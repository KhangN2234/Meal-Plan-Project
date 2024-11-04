from meal_app import app, db
from flask import Flask, render_template, request, redirect, session, flash
from spellchecker import SpellChecker
import requests
import os
from flask import Blueprint
from urllib.parse import quote
from flask import send_file
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io


recipe_search_app_id = os.getenv('RECIPE_SEARCH_APP_ID')
recipe_search_api_key = os.getenv('RECIPE_SEARCH_API_KEY')


@app.route('/download_pdf', methods=['POST'])
def download_pdf():
    if 'user' in session:  # Check if the user is logged in
        email = session['user']
        doc_ref = db.collection('users').document(email)
        user_data = doc_ref.get().to_dict()
        saved_recipes = user_data.get('cart', [])

        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)

        p.drawString(100, 750, "Shopping Cart Items:")
        y = 730
        
        ingredients = {}

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
                        measure = "x"
                    quantity = round(item.get('quantity', 0), 2)
                    food = item.get('food', "Unknown")

                    key = (food, measure)
                    
                    if key in ingredients:
                        ingredients[key]['quantity'] += quantity
                        ingredients[key]['recipes'].append(recipe_label)
                    else:
                        ingredients[key] = {
                            'quantity': quantity,
                            'measure': measure,
                            'food': food,
                            'recipes': [recipe_label]
                        }

        #Write to PDF
        for ingredient in ingredients.values():
            recipenames = ', '.join(ingredient['recipes'])
            p.drawString(100, y, f"{ingredient['quantity']} {ingredient['measure']} {ingredient['food']} (from {recipenames})")

            y -= 20  #Next line
            if y < 40:  #New page if needed
                p.showPage()
                y = 750  #Reset Y pos

        p.showPage()
        p.save()
        buffer.seek(0)

        #Send PDF as a response
        return send_file(buffer, as_attachment=True, download_name='shopping_cart.pdf', mimetype='application/pdf')
    else:
        return "Error: No user currently logged in.", 403