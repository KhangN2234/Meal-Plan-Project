from meal_app import app, db
from flask import Flask, render_template, request, redirect, session, flash
from spellchecker import SpellChecker
import requests
import os
from flask import Blueprint

recipe_search_app_id = os.getenv('RECIPE_SEARCH_APP_ID')
recipe_search_api_key = os.getenv('RECIPE_SEARCH_API_KEY')


@app.route('/download_pdf', methods=['POST'])
def download_pdf():
    if 'user' in session:  # Check if the user is logged in
        email = session['user']
        doc_ref = db.collection('users').document(email)
        user_data = doc_ref.get().to_dict()
        saved_recipes = user_data.get('cart', [])
        