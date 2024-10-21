from meal_app import app
from flask import Flask, render_template, request, redirect
from flask import Blueprint
import re

calorie_tracking_templates = Blueprint('calorie_tracking',__name__)

@app.route('/calorie_tracking')
def calorie_tracking():
    return render_template('calorie_tracking.html')
