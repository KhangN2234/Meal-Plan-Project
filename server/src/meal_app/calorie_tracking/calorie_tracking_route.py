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
    if 'user' not in session:
        flash("Please log in to track your calories.")
        return redirect('/login')

    user_email = session['user']
    user_ref = db.collection('users').document(user_email)
    calorie_entries_ref = user_ref.collection('calorie_entries')

    # Fetch user data and daily goal
    user_data = user_ref.get().to_dict() or {}
    daily_calorie_goal = int(user_data.get('daily_calorie_goal', 0))

    if request.method == 'POST':
        item_name = request.form.get('item_name', '').strip()
        total_calories = int(request.form.get('calories', '').strip())
        date = request.form.get('date', '').strip()
        if request.form.get('servings', '').strip():
            servings = int(request.form.get('servings', '').strip())
            calories = round(total_calories/servings)
        else:
            calories = total_calories

        if item_name and calories and date:
            try:
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

    # Retrieve entries grouped by date
    entries = {}
    docs = calorie_entries_ref.order_by('timestamp', direction=firestore.Query.DESCENDING).stream()
    for doc in docs:
        entry = doc.to_dict()
        entry_date = entry['date']
        if entry_date not in entries:
            entries[entry_date] = {'items': [], 'total_calories': 0}
        entries[entry_date]['items'].append({'id': doc.id, 'name': entry['item_name'], 'calories': entry['calories']})
        entries[entry_date]['total_calories'] += entry['calories']

    # Calculate today's total calories
    today_date = datetime.utcnow().strftime('%Y-%m-%d')
    
    total_calories_today = entries.get(today_date, {}).get('total_calories', 0)
    percentage = min((total_calories_today / daily_calorie_goal) * 100, 100) if daily_calorie_goal > 0 else 0

    calorie_difference = daily_calorie_goal - total_calories_today
    if calorie_difference > 300:
        comparison_message = f"You are {calorie_difference} calories under your daily goal.\nConsume a bit more calories to get within your goal!"
    elif calorie_difference > 0:
        comparison_message = f"You are {calorie_difference} calories under your daily goal.\nYou are on track for your goal!"
    elif calorie_difference < 300:
        comparison_message = f"You are {abs(calorie_difference)} calories over your daily goal.\nTry consuming less calorie dense meals to stay closer to your goal!"
    elif calorie_difference < 0:
        comparison_message = f"You are {abs(calorie_difference)} calories over your daily goal. \nYou reached your goal today!"
    else:
        comparison_message = "You have met your daily calorie goal exactly!"

    return render_template('calorie_tracking.html', entries=entries, daily_calorie_goal=daily_calorie_goal, total_calories_today=total_calories_today, percentage=percentage, comparison_message=comparison_message)
@app.route('/delete_entry', methods=['POST'])
def delete_entry():
    user_email = session.get('user')
    if user_email and 'entry_id' in request.form:
        entry_id = request.form['entry_id']
        user_ref = db.collection('users').document(user_email).collection('calorie_entries').document(entry_id)
        user_ref.delete()
    return redirect(url_for('calorie_tracking'))