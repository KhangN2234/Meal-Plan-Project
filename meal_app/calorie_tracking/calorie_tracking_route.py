from meal_app import app, db
from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask import Blueprint
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

# Define the blueprint
calorie_tracking_templates = Blueprint('calorie_tracking', __name__)
delete_entry_templates = Blueprint('delete_entry', __name__)
daily_calorie_goal_templates = Blueprint('daily_calorie_goal', __name__)

entries = {}
@app.route('/daily_calorie_goal', methods=['POST'])
def daily_calorie_goal():
    user_email = session['user']
    user_ref = db.collection('users').document(user_email)
    if request.method == 'POST':
        dailyCalorieGoal = request.form.get('calorie_goal')
        if dailyCalorieGoal:
            daily_calorie_Entry = {
                'daily_calorie_goal': dailyCalorieGoal
            }
            user_ref.set(daily_calorie_Entry)
        return redirect(url_for('calorie_tracking'))

@app.route('/calorie_tracking', methods=['GET', 'POST'])
def calorie_tracking():
    # Ensure user is logged in
    if 'user' not in session:
        flash("Please log in to track your calories.")
        return redirect('/login')

    user_email = session['user']
    user_ref = db.collection('users').document(user_email).collection('calorie_entries')

    if request.method == 'POST':
        # Get form data and validate it
        item_name = request.form.get('item_name', '').strip()
        calories = request.form.get('calories', '').strip()
        date = request.form.get('date', '').strip()

        # Only proceed if all fields are provided
        if item_name and calories and date:
            try:
                calories = int(calories)  # Convert calories to integer
            except ValueError:
                flash("Please enter a valid number for calories.")
                return redirect(url_for('calorie_tracking'))

            # Save entry to Firestore
            entry_data = {
                'item_name': item_name,
                'calories': calories,
                'date': date,
                'timestamp': datetime.utcnow()
            }
            user_ref.add(entry_data)  # Store entry under the user's calorie_entries collection

        else:
            flash('All fields are required!')

        return redirect(url_for('calorie_tracking'))

    # Retrieve all entries for this user from Firestore
    entries = {}
    docs = user_ref.stream()
    for doc in docs:
        entry = doc.to_dict()
        entry_date = entry.get('date')
        item_name = entry.get('item_name', 'Unnamed item')
        calories = entry.get('calories', 0)

        # Convert calories to int safely
        try:
            calories = int(calories)
        except ValueError:
            calories = 0

        if entry_date:
            if entry_date not in entries:
                entries[entry_date] = {'items': [], 'total_calories': 0}
            entries[entry_date]['items'].append({'name': item_name, 'calories': calories, 'id': doc.id})
            entries[entry_date]['total_calories'] += calories

    return render_template('calorie_tracking.html', entries=entries)
@app.route('/delete_entry', methods=['POST'])
def delete_entry():
    user_email = session.get('user')
    if user_email and 'entry_id' in request.form:
        entry_id = request.form['entry_id']
        user_ref = db.collection('users').document(user_email).collection('calorie_entries').document(entry_id)
        user_ref.delete()
    return redirect(url_for('calorie_tracking'))