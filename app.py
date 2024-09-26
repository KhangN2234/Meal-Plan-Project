from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')
if __name__ == '__main__':
    app.run(debug=True)