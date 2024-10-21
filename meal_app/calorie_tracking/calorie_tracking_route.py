from meal_app import app
from flask import Flask, render_template, request, redirect
from flask import Blueprint
from flask import url_for
import re

calorie_tracking_templates = Blueprint('calorie_tracking',__name__)

entries = {}

@app.route('/calorie_tracking', methods = ['GET','POST'])
def calorie_tracking():
    if request.method == 'POST':
        # Get form data
        item_name = request.form['item_name']
        calories = request.form['calories']
        date = request.form['date']

        # Store the entry by date in the dictionary
        if date not in entries:
            entries[date] = []

        entries[date].append({'name': item_name, 'calories': calories})

        # Redirect to avoid form resubmission on refresh
        return redirect(url_for('calorie_tracking'))

    # Render the page with the current entries
    return render_template('calorie_tracking.html', entries=entries)
