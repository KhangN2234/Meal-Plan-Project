from meal_app import app
from flask import Flask, render_template, request, redirect
from spellchecker import SpellChecker
import json
import sqlite3
import bcrypt
import requests
import os
import re
from flask import Blueprint

spell = SpellChecker()

search_templates = Blueprint('search',__name__)

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
        healthType = request.form['healthType']

        searchbarsplit = searchbar.split()
        misspelled = spell.unknown(searchbarsplit)
        corrected_words = [spell.correction(word) for word in misspelled]
        combinedcorrected = ' '.join(corrected_words)

        if(len(corrected_words) == 0):
            combinedcorrected = searchbar

        api_url = f"https://api.edamam.com/api/recipes/v2?type=any&q={combinedcorrected}&app_id={recipe_search_app_id}&app_key={recipe_search_api_key}&mealType={mealtype}&dishType={dishtype}&ingr={maxIngredients}&cuisineType={cuisineType}&health={healthType}&random=false&field=uri&field=label&field=calories&field=yield&field=ingredientLines&field=source&field=images&field=url&field=totalNutrients"

        response = requests.get(api_url)

        data = response.json()

        list_of_recipes = data['hits']

        display_data = [{'label': recipe['recipe']['label'], 'uri': recipe['recipe']['uri'], 'calories': round(recipe['recipe']['calories']), 'servings': round(recipe['recipe']['yield']), 'cal_per_serv': round(recipe['recipe']['calories']/recipe['recipe']['yield']), 'ingredients': recipe['recipe']['ingredientLines'], 'url': recipe['recipe']['url'], 'source': recipe['recipe']['source'], 'protein': round(recipe['recipe']['totalNutrients']['PROCNT']['quantity']), 'proteinunit': recipe['recipe']['totalNutrients']['PROCNT']['unit'], 'protein_per_serv': round(recipe['recipe']['totalNutrients']['PROCNT']['quantity']/recipe['recipe']['yield'])} for recipe in list_of_recipes]

        return render_template('search.html', searchbar=combinedcorrected,recipes=display_data, mealtype=mealtype, success=True)


