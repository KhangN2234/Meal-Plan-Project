from flask import Flask, render_template

app = Flask(__name__)

# Simple route that shows a message
@app.route('/')
def home():
    return "Welcome to the Meal App!"

if __name__ == '__main__':
    app.run(debug=True)
