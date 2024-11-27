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

email_templates = Blueprint('send_email', __name__)


def send_scheduled_email(user_email):
    # Check if the user is logged in
    try:
        # Fetch user data from Firestore
        doc_ref = db.collection('users').document(user_email)
        doc = doc_ref.get()
        if doc.exists:
            user_data = doc.to_dict()
            recipient_email = user_data.get('email')
            if recipient_email:
                # Email content
                sender_email = os.getenv("APP_EMAIL")
                app_password = os.getenv("EMAIL_APP_PASSWORD")
                subject = "Daily Prep Reminder!"
                body = """Hello,

                Here are the meals you have scheduled today!

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
