import sys 
sys.dont_write_bytecode = True

from flask import Flask
import firebase_admin
from firebase_admin import credentials, firestore
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import time

app = Flask(__name__)

app.secret_key = 'Qk!9:`6rb59G'  

cred = credentials.Certificate('meal-afe56-firebase-adminsdk-lsk0x-4f1be2c0c8.json')  
firebase_admin.initialize_app(cred)

db = firestore.client()

scheduler = BackgroundScheduler()
scheduler.start()

import meal_app.routes