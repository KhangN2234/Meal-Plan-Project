from meal_app import app
from flask import Flask, render_template, request, redirect
from flask import Blueprint
import re

calendar_templates = Blueprint('calendar',__name__)

@app.route('/calendar', methods=['GET', 'POST'])
def calendar():
    if request.method == 'GET': 
        return render_template('calendar.html')
    else:
        recipe_label = request.form.get('recipe_label')
        recipe_url = request.form.get('recipe_url')
        selected_days = request.form.getlist('selected_days')  # Get a list of selected days

        # Pass the selected days and recipe details to the template
        return render_template('calendar.html', recipe_label=recipe_label, recipe_url=recipe_url, selected_days=selected_days)