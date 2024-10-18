import sys 
sys.dont_write_bytecode = True

from flask import Flask
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)
cred = credentials.Certificate('meal-afe56-firebase-adminsdk-lsk0x-4f1be2c0c8.json')  
firebase_admin.initialize_app(cred)

db = firestore.client()

import meal_app.routes