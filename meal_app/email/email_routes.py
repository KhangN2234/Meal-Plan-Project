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
    