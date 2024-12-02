from meal_app import app, db
from flask import Flask, render_template, request, redirect, session, flash
from flask import Blueprint
from firebase_admin import firestore
import re
import os
import requests

from datetime import datetime

recipe_search_app_id = os.getenv('RECIPE_SEARCH_APP_ID')
recipe_search_api_key = os.getenv('RECIPE_SEARCH_API_KEY')

@app.route('/get_today_recipes', methods=['POST'])
def get_today_recipes():
    if 'user' in session:
        email = session['user']

        # Reference to the user's recipes collection
        recipes_collection_ref = db.collection('users').document(email).collection('recipes')
        
        print(recipes_collection_ref)

        # Get today's day of the week
        today = datetime.now().strftime('%A')  # e.g., 'Monday'

        # Fetch recipes scheduled for today
        recipes_today = [
            recipe.to_dict()
            for recipe in recipes_collection_ref.stream()
            if today in recipe.to_dict().get('days', [])
        ]

        # Gather details for console output
        recipe_names = [recipe['recipe_label'] for recipe in recipes_today]
        ingredients = []  # Assuming you'll add logic to fetch ingredients from the recipe data

        # Print details to the console
        print(f"Recipes scheduled for {today}: {recipe_names}")
        print(f"Ingredients needed: {ingredients}")  # Adjust as per recipe structure

        # Optionally flash a message for user feedback
        flash("Today's recipes and ingredients have been printed to the console.")

        # Redirect back to the profile
        return redirect('/profile')
    else:
        flash("Please log in to view today's recipes.")
        return redirect('/login')