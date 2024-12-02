from meal_app import app, db, scheduler, BackgroundScheduler
from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask import Blueprint
from datetime import datetime, timedelta
import firebase_admin
from firebase_admin import credentials, firestore
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import requests
from urllib.parse import quote

email_templates = Blueprint('send_email', __name__)
test_templates = Blueprint('test_route', __name__)

recipe_search_app_id = os.getenv('RECIPE_SEARCH_APP_ID')
recipe_search_api_key = os.getenv('RECIPE_SEARCH_API_KEY')

@app.route('/test_route', methods=['POST'])
def test_route():
    if request.method == 'POST':
        today = datetime.now().strftime('%A')
        
        email = session['user']
        recipes_collection_ref = db.collection('users').document(email).collection('recipes')
        recipes_collection_docs = recipes_collection_ref.stream()
        recipe_labels  = []
        total_ingredients = []

        for recipe in recipes_collection_docs:
            recipe_data = recipe.to_dict()
            if today in recipe_data.get('days', []):
                recipe_uri = recipe_data.get('recipe_uri')
                print(f"fetched uri: {recipe_uri}")

                api_uri = quote(recipe_uri, safe='')
                api_url = (
                    f"https://api.edamam.com/api/recipes/v2"
                    f"/by-uri?type=public&app_id={recipe_search_app_id}&app_key={recipe_search_api_key}&uri={api_uri}"
                )

                response = requests.get(api_url)

                if response.status_code == 200:
                    
                    recipe_json = response.json()
                    recipe_hits = recipe_json['hits']
                    for recipe in recipe_hits:
                        recipe_labels.append(recipe["recipe"]["label"])
                        recipe_ingredients = recipe["recipe"]["ingredientLines"]

                        for item in recipe_ingredients:
                            total_ingredients.append(item)
                    
                else:
                    print(f"Failed to fetch recipe details: {response.status_code} - {response.text}")
        print("Today's recipes:")
        for item in recipe_labels:
            print(f" - {item}")
        print("Total ingredients:")
        for item in total_ingredients:
            print(f" - {item}")


        return redirect('/profile')

def send_scheduled_email(user_email):
    # Check if the user is logged in
    
    today = datetime.now().strftime('%A')
        
    email = user_email
    recipes_collection_ref = db.collection('users').document(email).collection('recipes')
    recipes_collection_docs = recipes_collection_ref.stream()
    recipe_labels  = []
    total_ingredients = []

    for recipe in recipes_collection_docs:
        recipe_data = recipe.to_dict()
        if today in recipe_data.get('days', []):
            recipe_uri = recipe_data.get('recipe_uri')
            print(f"fetched uri: {recipe_uri}")

            api_uri = quote(recipe_uri, safe='')
            api_url = (
                f"https://api.edamam.com/api/recipes/v2"
                f"/by-uri?type=public&app_id={recipe_search_app_id}&app_key={recipe_search_api_key}&uri={api_uri}"
            )

            response = requests.get(api_url)

            if response.status_code == 200:
                    
                recipe_json = response.json()
                recipe_hits = recipe_json['hits']
                for recipe in recipe_hits:
                    recipe_labels.append(recipe["recipe"]["label"])
                    recipe_ingredients = recipe["recipe"]["ingredientLines"]

                    for item in recipe_ingredients:
                        total_ingredients.append(item)
                    
            else:
                print(f"Failed to fetch recipe details: {response.status_code} - {response.text}")

    try:
        # Fetch user data from Firestore
        doc_ref = db.collection('users').document(user_email)
        doc = doc_ref.get()
        if doc.exists:
            user_data = doc.to_dict()
            recipient_email = user_data.get('email')
            if recipient_email:

                recipe_labels_str = "\n * ".join(recipe_labels)
                total_ingredients_str = "\n * ".join(total_ingredients)

                # Email content
                sender_email = os.getenv("APP_EMAIL")
                app_password = os.getenv("EMAIL_APP_PASSWORD")
                subject = "Daily Prep Reminder!"
                body = f"""Hello!

Here are the meals you have scheduled today!
 * {recipe_labels_str}

Here's all the ingredients you'll need!
Make sure you've got all these items, thawed and/or prepared for the day!
 * {total_ingredients_str}

 Missing something?
 try out our shopping list generator and take it to the store with you!

Regards,
Meal App Team"""

                # Set up the email
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = recipient_email
                msg['Subject'] = subject
                msg.attach(MIMEText(body, 'plain'))

                # Send the email
                with smtplib.SMTP("smtp.gmail.com", 587) as server:
                    server.starttls()
                    server.login(sender_email, app_password)
                    server.sendmail(sender_email, recipient_email, msg.as_string())

                print(f"Email sent to {recipient_email}")

                now = datetime.now()
                next_run_time = now + timedelta(days=1)
                scheduler.add_job(
                    send_scheduled_email,
                    'date',
                    run_date=next_run_time.replace(hour=now.hour, minute=now.minute,second=now.second, microsecond=now.microsecond),
                    args=[user_email]
                )   
                print(f"Next email scheduled for {recipient_email} at {next_run_time.strftime('%Y-%m-%d %H:%M:%S')}")

            else:
                print(f"No email found for user {user_email}")
        else:
            print(f"User {user_email} does not exist in the database.")
    except Exception as e:
        print(f"Error sending email: {str(e)}")

def schedule_email(user_email, schedule_time):
    # Convert scheduled time to datetime object
    today = datetime.now().date()
    scheduled_time = datetime.strptime(schedule_time, "%H:%M").replace(year=today.year, month=today.month, day=today.day)
    now = datetime.now()
    print(scheduled_time)
    print(now)
    # Calculate the delay until the scheduled time
    delay = (scheduled_time - now).total_seconds()
    print(delay)
    # If the scheduled time is in the future, schedule the email to send at that time
    if delay > 0:
        scheduler.add_job(
            send_scheduled_email,
            'date',
            run_date=now + timedelta(seconds=delay),
            args=[user_email]
        )
        print(f"Email scheduled for {user_email} at {scheduled_time}")
    else:
        print("Scheduled time has already passed. Please choose a time in the future.")
