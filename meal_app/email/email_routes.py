from meal_app import app, db
from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask import Blueprint
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


@app.route('/send-email', methods=['POST'])
def send_email():
    if 'user' not in session:
        flash("You need to log in to send an email.")
        return redirect ('/login')

    #Get the logged-in user's email
    email = session['user']
    doc_ref = db.collection('users').document(email)
    doc = doc_ref.get()

    if not doc.exists:
        flash('user information not found')
        return redirect('/profile')
    
    user_data = doc.to_dict()
    recipient_email = user_data.get('email')

    if not recipient_email:
        flash('No email address found for teh user.')
        return redirect("/profile")
    
    try:
        #Email content
        sender_email = "MealApp0@gmail.com"
        app_password = "cqal ozgh cofo tjvt"
        subject = "Daily Prep Reminder!"
        body = """Hello1,

        Here are the meals you have scheduled today!

        Regards,
        Meal App Team"""

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
    except Exception as e:
        flash(f"Failed to send email: {str(e)}")
    return redirect('/profile')