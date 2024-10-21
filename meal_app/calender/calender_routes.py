from meal_app import app
from flask import Flask, render_template, request, redirect
from flask import Blueprint
import re

calender_templates = Blueprint('calender',__name__)

@app.route('/')
def calender():
    return render_template('calender.html')