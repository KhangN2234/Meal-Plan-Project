from meal_app import app, db
from flask import Flask, render_template, request, redirect, session, flash
from flask import Blueprint
from firebase_admin import firestore
import re
import json

calendar_templates = Blueprint('calendar',__name__)

@app.route('/calendar', methods=['GET', 'POST'])
def calendar():
    if request.method == 'GET': 
        if 'user' in session:
            email = session['user']

            # Reference to the user's recipes collection
            recipes_collection_ref = db.collection('users').document(email).collection('recipes')
            recipes_docs = recipes_collection_ref.stream()
            
            
            # Check if the 'recipes' collection is empty
            if not any(True for _ in recipes_docs):
                return redirect('search')
            
            # Display the recipes in the calendar
            data = [
            {
                'label': recipe.to_dict().get('recipe_label'),
                'days': recipe.to_dict().get('days'),
                'url': recipe.to_dict().get('recipe_url')
            }
            for recipe in recipes_collection_ref.get()]
            
            return render_template('calendar.html', 
                                   recipes_list = data,
                                   recipe_label = None,
                                   )
        else:
            flash("Please log in to access your calendar.")
            return redirect('/login')
    
    # Handle method POST
    else:
        if 'user' in session:
            email = session['user']

            # Reference to the user's recipes collection
            recipes_collection_ref = db.collection('users').document(email).collection('recipes')
            recipes_docs = recipes_collection_ref.stream()
            
            
    # This portion add the new recipe to the firebase 
            recipe_label = request.form.get('recipe_label')
            recipe_url = request.form.get('recipe_url')
            selected_days = request.form.getlist('selected_days')
            recipe_ingredients_json = request.form.get('recipe_ingredients')

            recipe_ingredients = json.loads(recipe_ingredients_json)
            
            if recipe_label != 'None':
                if not selected_days:
                    print("list empty")
                else:
                    recipe_data = {
                        'recipe_label': recipe_label,
                        'recipe_url': recipe_url,
                        'days': selected_days,
                        'ingredients': recipe_ingredients
                    }
                    print(recipe_data)
                    # Save to firebase
                    print('ingredient list: ', recipe_ingredients)
                    recipes_collection_ref.document(recipe_label).set(recipe_data)
                    flash(f"Succesfully added Recipe: {recipe_label}")

            

            
    # This portion will display the data in the firebase
            # Display the recipes in the calendar
            data = [
            {
                'label': recipe.to_dict().get('recipe_label'),
                'days': recipe.to_dict().get('days'),
                'url': recipe.to_dict().get('recipe_url')
            }
            for recipe in recipes_collection_ref.get()]

            return render_template('calendar.html', 
                                   recipes_list = data,
                                   recipe_label = recipe_label,
                                   recipe_url = recipe_url,
                                   selected_days = selected_days
                                   )
        else:
            flash("Please log in to access your calendar.")
            return redirect('/login')
            
            