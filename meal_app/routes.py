from meal_app import app
from flask import Flask, render_template, request, redirect
import json
import sqlite3
import bcrypt
import requests
import os
import re
from .scale_recipe.scale_recipe_routes import scaled_recipe_templates
from .scale_recipe.recipe_scaling_routes import recipe_scaling_templates
from .search_recipe.search_routes import search_templates


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



app.register_blueprint(search_templates)
app.register_blueprint(scaled_recipe_templates)
app.register_blueprint(recipe_scaling_templates)