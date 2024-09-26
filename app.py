from flask import Flask, render_template, request, redirect
import sqlite3
import bcrypt

app = Flask(__name__)

# Initialize the database (if not already)
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

init_db()

# Route to display the signup form and handle form submissions
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Hash the password before storing it
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Store the username and password in the database
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            return redirect('/success')  # Redirect after successful signup
        except sqlite3.IntegrityError:
            return "Username already exists. Try another one."
        finally:
            conn.close()
    
    return render_template('signup.html')

# Success page
@app.route('/success')
def success():
    return "Account created successfully!"

if __name__ == '__main__':
    app.run(debug=True)
