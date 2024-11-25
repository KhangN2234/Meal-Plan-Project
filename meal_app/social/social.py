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

social_template = Blueprint('social', __name__)

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
    
    posts = db.collection('posts').order_by('timestamp', direction='DESCENDING').stream()
    userPosts = [
        {'content': post.to_dict().get('content'),
         'author': post.to_dict().get('author'),
         'email': post.to_dict().get('email'),
         'timestamp': post.to_dict().get('timestamp')}
        for post in posts
    ]
    

    
    return render_template('social.html', user_data=user_data, userPosts=userPosts)
