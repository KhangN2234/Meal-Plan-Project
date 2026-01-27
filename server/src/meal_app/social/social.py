from meal_app import app, db
from flask import Flask, render_template, request, redirect, session, flash
from flask import Blueprint
import json
import sqlite3
import bcrypt
import requests
import os
import re
from datetime import datetime
from urllib.parse import quote

recipe_search_app_id = os.getenv('RECIPE_SEARCH_APP_ID')
recipe_search_api_key = os.getenv('RECIPE_SEARCH_API_KEY')

social_template = Blueprint('social', __name__)
postRecipe_template = Blueprint('postRecipe', __name__)

@app.route('/social', methods=['GET', 'POST'])
def social():
    if 'user' not in session:
        flash("Please log in to access your account information")
        return redirect('/login')
    
    email = session['user']
    doc_ref = db.collection('users').document(email)
    doc = doc_ref.get()

    if not doc.exists:
        return redirect('/login')
    
    user_data = doc.to_dict()


    friendsList = user_data.get('friends', [])
    if friendsList is None:
        friendsList = []

    
    posts = list(db.collection('posts').order_by('timestamp', direction='DESCENDING').stream())
    userPosts = [
        {'content': post.to_dict().get('content'),
         'author': post.to_dict().get('author'),
         'email': post.to_dict().get('email'),
         'timestamp': post.to_dict().get('timestamp')}
        for post in posts
    ]
    
    friendPosts = [
        {'content': post.to_dict().get('content'),
         'author': post.to_dict().get('author'),
         'email': post.to_dict().get('email'),
         'timestamp': post.to_dict().get('timestamp')}
        for post in posts if post.to_dict().get('email') in friendsList
    ]
    
    friendsOnly = request.args.get('friendsOnly', '').lower() == 'true'
    
    return render_template('social.html', user_data=user_data, userPosts=userPosts, friendPosts=friendPosts, friendsOnly=friendsOnly)

@app.route('/postrecipe', methods=['GET', 'POST'])
def postRecipe():
    recipeURI = request.form.get('recipeURI')

    api_url = f"https://api.edamam.com/api/recipes/v2/by-uri?type=public&app_id={recipe_search_app_id}&app_key={recipe_search_api_key}&uri="
    encodedString = quote(recipeURI, safe='')
    api_url += encodedString

    response = requests.get(api_url)
    data = response.json()
    print(data)
    recipe = data['hits'][0]['recipe']

    print("Recipe = ", recipe)

    
    post = (
        f"Check this out!\n"
        f"{recipe['label']}.\n "
        f"It has {round(recipe['calories'] / recipe['yield'])} calories/serving\n "
        f"and {round(recipe['totalNutrients']['PROCNT']['quantity'] / recipe['yield'])}g of protein/serving. "
        f"Link: {recipe['url']}"
    )

    
    if 'user' not in session:
        flash("Please log in to share")
        return redirect('/login')
    
    email = session['user']
    doc_ref = db.collection('users').document(email)
    doc = doc_ref.get()

    if not doc.exists:
        return redirect('/login')
    
    username = doc.to_dict().get('username')
    if username == "":
        username = "UnknownUsername"
    post_entry = {
        'author': username,
        'email': email,
        'content': post,
        'timestamp': datetime.utcnow(),
    }
    db.collection('posts').add(post_entry)

    

    return redirect('/social')

    
