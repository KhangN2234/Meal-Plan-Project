from meal_app import app
from flask import Flask, render_template, request, redirect, session, flash
from flask import Blueprint
from flask import url_for
import re
from datetime import  datetime
import firebase_admin
from firebase_admin import credentials, firestore
from __init__ import db

calorie_tracking_templates = Blueprint('calorie_tracking',__name__)

entries = {}

@app.route('/calorie_tracking', methods=['GET', 'POST'])
def calorie_tracking():
    # Ensure user is logged in
    if 'user' not in session:
        flash("Please log in to track your calories.")
        return redirect('/login')

    user_email = session['user']
    user_ref = db.collection('users').document(user_email).collection('calorie_entries')

    if request.method == 'POST':
        # Get form data
        item_name = request.form['item_name']
        calories = int(request.form['calories'])
        date = request.form['date']

        # Save entry to Firestore
        entry_data = {
            'item_name': item_name,
            'calories': calories,
            'date': date,
            'timestamp': datetime.utcnow()
        }
        user_ref.add(entry_data)  # Store entry under the user's calorie_entries collection

        flash('Entry added successfully!')
        return redirect(url_for('calorie_tracking'))

    # Retrieve all entries for this user from Firestore
    entries = {}
    docs = user_ref.stream()
    for doc in docs:
        entry = doc.to_dict()
        entry_date = entry['date']
        if entry_date not in entries:
            entries[entry_date] = {'items': [], 'total_calories': 0}
        entries[entry_date]['items'].append({'name': entry['item_name'], 'calories': entry['calories']})
        entries[entry_date]['total_calories'] += entry['calories']

    return render_template('calorie_tracking.html', entries=entries)