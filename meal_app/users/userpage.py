from meal_app import app, db
from flask import Flask, render_template, request, redirect, session, flash, Blueprint
import json
import sqlite3
import bcrypt
import requests
import os
import re
from datetime import datetime


user_template = Blueprint('user',__name__)

recipe_search_app_id = os.getenv('RECIPE_SEARCH_APP_ID')
recipe_search_api_key = os.getenv('RECIPE_SEARCH_API_KEY')

@app.route('/user/<userEmail>', methods=['GET', 'POST'])
def user(userEmail):
    user_ref = db.collection('users').document(userEmail)
    user_doc = user_ref.get()

    if user_doc.exists:
        user_data = user_doc.to_dict()
        posts = db.collection('posts').where('email', '==', userEmail).order_by('timestamp', direction='DESCENDING').stream()
        userPosts = [
            {'content': post.to_dict().get('content'),
            'author': post.to_dict().get('author'),
            'email': post.to_dict().get('email'),
            'timestamp': post.to_dict().get('timestamp')}
            for post in posts
        ]
        return render_template('userpage.html', username=userEmail, user_data=user_data, userPosts=userPosts)
    else:
        flash("User not found!")
        return redirect('/')

