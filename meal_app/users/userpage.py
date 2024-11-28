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

    viewingSelf = False

    loggedInUser = session['user']

    if loggedInUser == userEmail:
        viewingSelf = True

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
        recipes_collection_ref = db.collection('users').document(userEmail).collection('recipes')

        data = [
            {
                'label': recipe.to_dict().get('recipe_label'),
                'days': recipe.to_dict().get('days'),
                'url': recipe.to_dict().get('recipe_url')
            }
            for recipe in recipes_collection_ref.get()]

        loggedInUserRef = db.collection('users').document(loggedInUser)
        loggedInUserDoc = loggedInUserRef.get()
        loggedInUserData = loggedInUserDoc.to_dict()

        friendsList = loggedInUserData.get('friends', [])
        if friendsList is None:
            friendsList = []

        friendsWithDetails = []
        for friendEmail in friendsList:
            friend_doc = db.collection('users').document(friendEmail).get()
            if friend_doc.exists:
                friend_data = friend_doc.to_dict()
                friendsWithDetails.append({
                    'email': friendEmail,
                    'username': friend_data.get('username', 'Unknown') #Default if username not found
                })

        friendsWith = userEmail in friendsList

        viewedUserFriendsList = []
        viewedUserFriends = user_doc.to_dict().get('friends', [])
        for friendEmail in viewedUserFriends:
            friend_doc = db.collection('users').document(friendEmail).get()
            if friend_doc.exists:
                friend_data = friend_doc.to_dict()
                viewedUserFriendsList.append({
                    'email': friendEmail,
                    'username': friend_data.get('username', 'Unknown')  #Default if username not found
                })

        print(viewedUserFriendsList)
        
        return render_template('userpage.html', username=userEmail, user_data=user_data, userPosts=userPosts, calendarRecipes=data, viewingSelf=viewingSelf, friendsWith = friendsWith, viewedUserFriendsList=viewedUserFriendsList)
    else:
        flash("User not found!")
        return redirect('/')

@app.route('/friend/<userEmail>', methods=['POST'])
def friend(userEmail):
    if 'user' in session:
        email = session['user']
        
        # Get the user document
        user_doc_ref = db.collection('users').document(email)
        user_doc = user_doc_ref.get()

        print(user_doc)
        
        # Check if the 'friends' field exists and has items
        if user_doc.exists:
            friendsList = user_doc.to_dict().get('friends', [])
        else: 
            user_doc.update({'friends': []})
            friendsList = []

        if userEmail in friendsList:
            friendsList.remove(userEmail)
        else:
            friendsList.append(userEmail)

        user_doc_ref.update({'friends': friendsList})
        print(user_doc.to_dict().get('friends', []))

        return redirect(f'/user/{userEmail}')
    else:
        return redirect(f'/user/{userEmail}')
        




