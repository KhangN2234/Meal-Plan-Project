from meal_app import app
from flask import Flask, render_template, request, redirect
import json
import sqlite3
import bcrypt
import requests
import os



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
            return redirect('/success')  # Redirect after successful signup
        except sqlite3.IntegrityError:
            return "Username already exists. Try another one."
        finally:
            conn.close()
    
    return render_template('signup.html')
# Success page
@app.route('/success')
def success():
    return "Account created successfully!"

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
        api_url = f"https://api.edamam.com/api/recipes/v2?type=any&q={searchbar}&app_id={recipe_search_app_id}&app_key={recipe_search_api_key}&mealType={mealtype}&random=false&field=uri&field=label&field=calories&field=yield&field=ingredientLines&field=source&field=images&field=url&field=totalNutrients"

        response = requests.get(api_url)

        data = response.json()

        list_of_recipes = data['hits']

        display_data = [{'label': recipe['recipe']['label'], 'calories': round(recipe['recipe']['calories']), 'servings': round(recipe['recipe']['yield']), 'cal_per_serv': round(recipe['recipe']['calories']/recipe['recipe']['yield']), 'ingredients': recipe['recipe']['ingredientLines'], 'url': recipe['recipe']['url'], 'source': recipe['recipe']['source'], 'protein': round(recipe['recipe']['totalNutrients']['PROCNT']['quantity']), 'proteinunit': recipe['recipe']['totalNutrients']['PROCNT']['unit'], 'protein_per_serv': round(recipe['recipe']['totalNutrients']['PROCNT']['quantity']/recipe['recipe']['yield'])} for recipe in list_of_recipes]
        

        return render_template('search.html', recipes=display_data, mealtype=mealtype, searchbar=searchbar, success=True)