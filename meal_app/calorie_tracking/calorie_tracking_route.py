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
            try:
                # Safely update only the `daily_calorie_goal` field
                user_ref.update({'daily_calorie_goal': int(dailyCalorieGoal)})
                flash("Daily calorie goal updated successfully!")
            except Exception as e:
                flash(f"Error updating daily calorie goal: {str(e)}")
        return redirect(url_for('calorie_tracking'))

@app.route('/calorie_tracking', methods=['GET', 'POST'])
def calorie_tracking():
    # Ensure user is logged in
    if 'user' not in session:
        flash("Please log in to track your calories.")
        return redirect('/login')

    user_email = session['user']
    user_ref = db.collection('users').document(user_email)
    calorie_entries_ref = user_ref.collection('calorie_entries')

    # Retrieve daily calorie goal
    daily_calorie_goal = None
    try:
        user_data = user_ref.get()
        if user_data.exists:
            daily_calorie_goal = user_data.to_dict().get('daily_calorie_goal', None)
    except Exception as e:
        flash(f"Error retrieving daily calorie goal: {str(e)}")

    # Handle POST request for adding a calorie entry
    if request.method == 'POST':
        item_name = request.form.get('item_name', '').strip()
        calories = request.form.get('calories', '').strip()
        date = request.form.get('date', '').strip()

        if item_name and calories and date:
            try:
                calories = int(calories)
                entry_data = {
                    'item_name': item_name,
                    'calories': calories,
                    'date': date,
                    'timestamp': datetime.utcnow()
                }
                calorie_entries_ref.add(entry_data)
                flash("Entry added successfully!")
            except ValueError:
                flash("Please enter a valid number for calories.")
            except Exception as e:
                flash(f"Error adding entry: {str(e)}")
        else:
            flash("All fields are required!")

        return redirect(url_for('calorie_tracking'))

    # Retrieve all calorie entries and calculate today's total calories
    entries = {}
    total_calories_today = 0
    try:
        today = datetime.utcnow().strftime('%Y-%m-%d')
        docs = calorie_entries_ref.stream()
        for doc in docs:
            entry = doc.to_dict()
            entry_date = entry.get('date')
            item_name = entry.get('item_name', 'Unnamed item')
            calories = entry.get('calories', 0)

            try:
                calories = int(calories)
            except ValueError:
                calories = 0

            if entry_date:
                if entry_date not in entries:
                    entries[entry_date] = {'items': [], 'total_calories': 0}
                entries[entry_date]['items'].append({'name': item_name, 'calories': calories, 'id': doc.id})
                entries[entry_date]['total_calories'] += calories

                # Add calories to today's total if the entry date matches
                if entry_date == today:
                    total_calories_today += calories
    except Exception as e:
        flash(f"Error retrieving entries: {str(e)}")

    # Pass daily calorie goal and today's total to the template
    return render_template('calorie_tracking.html', entries=entries, daily_calorie_goal=daily_calorie_goal, total_calories_today=total_calories_today)
@app.route('/delete_entry', methods=['POST'])
def delete_entry():
    user_email = session.get('user')
    if user_email and 'entry_id' in request.form:
        entry_id = request.form['entry_id']
        user_ref = db.collection('users').document(user_email).collection('calorie_entries').document(entry_id)
        user_ref.delete()
    return redirect(url_for('calorie_tracking'))