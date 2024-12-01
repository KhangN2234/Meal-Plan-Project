from meal_app import app, db
from flask import Flask, render_template, request, redirect, session, flash
import json
import sqlite3
import bcrypt
import requests
import os
import re
import random
from .scale_recipe.scale_recipe_routes import scaled_recipe_templates
from .scale_recipe.recipe_scaling_routes import recipe_scaling_templates
from .search_recipe.search_routes import search_templates
from .shopping_cart.shopping_cart_route import shopping_cart_template
from .calendar.calendar_routes import calendar_templates
from .shopping_cart.download_pdf import download_pdf
from .calorie_tracking.calorie_tracking_route import calorie_tracking_templates
from .calorie_tracking.calorie_tracking_route import delete_entry_templates
from .calorie_tracking.calorie_tracking_route import daily_calorie_goal_templates
from .email.email_routes import email_templates
from .social.social import social_template
from .users.userpage import user_template
from datetime import datetime
from meal_app.meal_api import fetch_meals_by_category
from .email.email_routes import schedule_email,send_scheduled_email


@app.route('/')
def startup():
    return redirect('/login')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')
# test
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
            'password': hashed_password.decode('utf-8'),
            'username': '',  
            'bio': '',  
            'profile_picture': ''  
        }

        try:
            # Store user data in Firebase Firestore using the email as document ID
            db.collection('users').document(email).set(user_data)

            flash('Account created successfully!')
            session['new_signup'] = True
            session['user'] = email
            return redirect('/profile')
        
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

                if 'new_signup' in session:
                    session.pop('new_signup', None)
                    flash('Account created successfully!')
                else:
                    flash('You have been successfully logged in!')
                return redirect('/profile')
        else:
                # If its incorrect
                flash('Invalid password')
                return render_template('login.html')
        
        flash('No account found with this email')
        return render_template('login.html')
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    # This removes the user from the session if he is logged in
    session.pop('user', None)

    flash('You have been successfully logged out.')

    return redirect('/login')

@app.route('/profile', methods=['GET', 'POST'])
def profile():

    if 'user' not in session:
        flash("Please log in to access your account information")
        return redirect('/login')
    
    email = session['user']
    doc_ref = db.collection('users').document(email)
    doc = doc_ref.get()

    if not doc.exists:
        return redirect('/login')
    
    user_data = doc.to_dict()

    if request.method == 'POST':
        username = request.form.get('username', user_data.get('username'))
        bio = request.form.get('bio', user_data.get('bio'))
        password = request.form.get('password')
        newPost = request.form.get('newPost')
        opt_in_out = 'opt_in_out' in request.form
        email_scheduled_time = request.form.get('email_scheduled_time')

        if not email_scheduled_time:
            print("No email schedule time recieved!")
            
        if newPost:
            if username == "":
                username = "UnknownUsername"
            postData = {
                'author': username,
                'email': email,
                'content': newPost,
                'timestamp': datetime.utcnow()
            }

            db.collection('posts').add(postData)
            return redirect('/social')

        if bio:
            if request.form.get('bio') != user_data.get('bio'):

                username = doc.to_dict().get('username')
                if username == "":
                    username = "UnknownUsername"
                post_entry = {
                    'author': username,
                    'email': email,
                    'content': "Updated bio to: \" " + request.form.get('bio') + " \"",
                    'timestamp': datetime.utcnow(),
                }
                db.collection('posts').add(post_entry)

            updated_data = {
                'username': username,
                'bio': bio,
                'opt_in_out': opt_in_out,
                'email_scheduled_time': email_scheduled_time
            }

        if password:
            # Hash the new password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            updated_data['password'] = hashed_password.decode('utf-8')
     
        doc_ref.update(updated_data)

        schedule_email(email, email_scheduled_time)

        flash('Profile updated successfully!')

        
        return redirect('/profile')
    
    posts = db.collection('posts').where('email', '==', email).order_by('timestamp', direction='DESCENDING').stream()
    userPosts = [
        {'content': post.to_dict().get('content'),
         'author': post.to_dict().get('author'),
         'email': post.to_dict().get('email'),
         'timestamp': post.to_dict().get('timestamp')}
        for post in posts
    ]
    

    
    return render_template('profile.html', user_data=user_data, userPosts=userPosts)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        if name and email and message:
            contact_data = {
                'name': name,
                'email': email,
                'message': message,
                'timestamp': datetime.utcnow()
        }

            db.collection('contacts').add(contact_data)
            flash('Your message has been sent successfully!')

        else:
            flash('Error, your message did not send please fill out the boxes above!')

            return redirect('/contact')
    
    return render_template('contact.html')

@app.route('/popular-meals')
def popular_meals():
    categories = ["Beef", "Chicken", "Dessert", "Seafood", "Vegetarian"]
    popular_meals = []

    for category in categories:
        meals = fetch_meals_by_category(category)
        if meals:
            random_meal = random.choice(meals)  # Select a random meal
            popular_meals.append({
                "category": category,
                "meal": random_meal
            })

    return render_template('popular_meals.html', popular_meals=popular_meals)

app.register_blueprint(search_templates)
app.register_blueprint(scaled_recipe_templates)
app.register_blueprint(recipe_scaling_templates)
app.register_blueprint(shopping_cart_template)
app.register_blueprint(calendar_templates)
app.register_blueprint(calorie_tracking_templates)
app.register_blueprint(delete_entry_templates)
app.register_blueprint(daily_calorie_goal_templates)
app.register_blueprint(social_template)
app.register_blueprint(user_template)
app.register_blueprint(email_templates)