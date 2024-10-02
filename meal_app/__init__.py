import sys 
sys.dont_write_bytecode = True
from flask import Flask


app = Flask(__name__)


import meal_app.routes