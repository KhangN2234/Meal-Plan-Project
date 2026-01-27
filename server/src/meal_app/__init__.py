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

cred = credentials.Certificate('meal-afe56-d805a28a48bf.json')  
firebase_admin.initialize_app(cred)

db = firestore.client()

scheduler = BackgroundScheduler()
scheduler.start()

import meal_app.routes