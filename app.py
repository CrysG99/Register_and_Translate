from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql #type: ignore
import re

app = Flask(__name__)
app.secret_key = 'jonakey'


db_config = {
    'host': '10.2.3.123',
    'user': 'jonathan',
    'password': 'jonathan2007',
    'database': 'book_store'
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        try:
            conn = pymysql.connect(**db_config)
            cursor = conn.cursor()
            query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, email, password))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect('/')
        except Exception as e:
            flash('Email already exists or another error occurred.', 'danger')
            print(f"Error: {e}")
            return redirect(url_for('register'))
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        conn = pymysql.connect(**db_config)
        cur = conn.cursor()
        cur.execute("SElECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            flash('Logget inn! Velkommen {username}', 'suksess')
            return redirect(url_for('home'))
        else:
            flash('Ugyldig brukernavn eller passord', 'danger')
            print(f"Error: {e}")
            
    return render_template('login.html')

@app.route('/order')
def order():
    return render_template('order.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)