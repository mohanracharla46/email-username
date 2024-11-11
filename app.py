import os
from flask import Flask, render_template, request
import sqlite3
import random 


app = Flask(__name__)


def get_db_connection():
    db_file = os.path.join(app.root_path, 'users.db')
    conn = sqlite3.connect(db_file)
    return conn

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT UNIQUE, username TEXT UNIQUE)''')

    if request.method == 'POST':
        email = request.form['email']
        
        c.execute("SELECT username FROM users WHERE email = ?", (email,))
        existing_user = c.fetchone()
        if existing_user:
            username = existing_user[0]
        else:
            username_base = email.split('@')[0]
            username_number = random.randint(10, 99)
            username = f"{username_base}{username_number}"
            c.execute("SELECT username FROM users WHERE username = ?", (username,))
            while c.fetchone():
                username += '_'
            
            c.execute("INSERT INTO users (email, username) VALUES (?, ?)", (email, username))
            conn.commit()
        
        conn.close()
        return render_template('index.html', username=username)
    
    conn.close()
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)