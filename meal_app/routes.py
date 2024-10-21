from meal_app import app#, db
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
from .shopping_cart.shopping_cart_route import shopping_cart_template


@app.route('/')
def welcome():
    return render_template('welcome.html')

# Route to display the signup form and handle form submissions
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Hash the password before storing it
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Create user data to store in Firestore
        #user_data = {
        #    'email': email,
        #    'password': hashed_password.decode('utf-8')  # Store hashed password
        #}

        try:
            # Store user data in Firebase Firestore using the email as document ID
            #db.collection('users').document(email).set(user_data)
            return render_template('signup.html', success=True)
        except Exception as e:
            return render_template('signup.html', success=False, error=str(e))
    
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
app.register_blueprint(shopping_cart_template)