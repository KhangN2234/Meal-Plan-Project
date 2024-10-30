from meal_app import app, db
from flask import Flask, render_template, request, redirect, session
from flask import Blueprint
from firebase_admin import firestore
import re

calendar_templates = Blueprint('calendar',__name__)

@app.route('/calendar', methods=['GET', 'POST'])
def calendar():
    if request.method == 'GET': 
        print("get")
        if 'user' in session:
            # Structure to save in Firebase
            print("success")
        return render_template('calendar.html')
    else:
        print("post")
        if 'user' in session:
            recipe_label = request.form.get('recipe_label')
            recipe_url = request.form.get('recipe_url')
            selected_days = request.form.getlist('selected_days')  # Get a list of selected days
            email = session['user']
            if 'recipes' != recipe_label:
                recipe_data = {
                    'recipe_label': recipe_label,
                    'recipe_url': recipe_url,
                    'days': selected_days
                }
                db.collection('users').document(email).collection('recipes').document(recipe_label).set(recipe_data)
            else:
                db.collection('users').document(email).collection('recipes').document(recipe_label).array('days').set(selected_days)
            
            # Pass the selected days and recipe details to the template
            return render_template('calendar.html', recipe_label=recipe_label, recipe_url=recipe_url, selected_days=selected_days)