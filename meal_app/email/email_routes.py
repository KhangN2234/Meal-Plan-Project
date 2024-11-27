from meal_app import app, db
from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask import Blueprint
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

email_templates = Blueprint('send_email', __name__)


@app.route('/send-email', methods=['GET'])
def send_email():
    # Check if the user is logged in
    if 'user' not in session:
        flash("You need to log in to send an email.")
        return redirect('/login')

    # Get the logged-in user's email
    email = session['user']
    doc_ref = db.collection('users').document(email)
    doc = doc_ref.get()

    if not doc.exists:
        flash("User information not found.")
        return redirect('/profile')
    
    user_data = doc.to_dict()
    recipient_email = user_data.get('email')

    if not recipient_email:
        flash("No email address found for the user.")
        return redirect("/profile")

    try:
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

        flash(f"Email successfully sent to {recipient_email}!")
    except Exception as e:
        flash(f"Failed to send email: {str(e)}")

    # Redirect back to the profile page
    return redirect('/profile')