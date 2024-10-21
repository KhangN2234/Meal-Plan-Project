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

    # You can now display the recipe name and URL on the calendar page
    return render_template('calendar.html', recipe_label=recipe_label, recipe_url=recipe_url)