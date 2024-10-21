from meal_app import app, db
from flask import Flask, render_template, request, redirect, session
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
        email = request.form['email']
        password = request.form['password']
        
        # Hash the password before storing it
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Create user data to store in Firestore
        user_data = {
            'email': email,
            'password': hashed_password.decode('utf-8')  # Store hashed password
        }

        try:
            # Store user data in Firebase Firestore using the email as document ID
            db.collection('users').document(email).set(user_data)
            return render_template('signup.html', success=True)
        except Exception as e:
            return render_template('signup.html', success=False, error=str(e))
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # This Gets the email and password from user
        email = request.form['email']
        password = request.form['password']

        # Checks to see if user has signed up
        doc_ref = db.collection('users').document(email)
        doc = doc_ref.get()

        if doc.exists:
            # Gets password
            user_data = doc.to_dict()
            stored_password = user_data['password']

            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                # If the pasword matches, set the user session
                session['user'] = email
                return redirect('/profile')  # Sends user to profile page if login works
            else:
                # error if the password is incorret
                return render_template('login.html', error="Invalid password")
        else:
            # Sends an error if no account exists for this email
            return render_template('login.html', error="No account found with this email")
        
    return render_template('login.html')

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