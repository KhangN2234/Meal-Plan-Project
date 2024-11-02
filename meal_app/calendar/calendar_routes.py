from meal_app import app, db
from flask import Flask, render_template, request, redirect, session
from flask import Blueprint
from firebase_admin import firestore
import re

calendar_templates = Blueprint('calendar',__name__)

@app.route('/calendar', methods=['GET', 'POST'])
def calendar():
    if request.method == 'GET': 
        if 'user' in session:
            email = session['user']

            # Reference to the user's recipes collection
            recipes_collection_ref = db.collection('users').document(email).collection('recipes')
            recipes_docs = recipes_collection_ref.stream()
            doc = db.collection('users').document(email).collection('recipes').get()
            
            # Check if the 'recipes' collection is empty
            if not any(True for _ in recipes_docs):
                return redirect('search')
            
            # Put name of recipes in an array list
            recipes_name = []
            #.to_dict() convert the variable to an array then .get() get the value (ie recipe_url) from that map created from the document
            for recipe in doc:
                recipes_name.append(recipe.to_dict().get('recipe_label'))


            data = [{'label': recipes_collection_ref.document(recipe).get().to_dict().get('recipe_label'), 
                     'days' : recipes_collection_ref.document(recipe).get().to_dict().get('days'),
                     'url' : recipes_collection_ref.document(recipe).get().to_dict().get('recipe_url')} for recipe in recipes_name]
            
            #recipes_list = [{'label': db.collection('users').document(email).collection('recipes').document(recipe).get().to_dict().get('recipe_label')} for recipe in recipes_name]
            return render_template('calendar.html', 
                                   recipes_list = data
                                   )
        else:
            return redirect('/login')
    
    else:
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