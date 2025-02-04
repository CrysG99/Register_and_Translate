from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql #type: ignore
from flask import session
import re

app = Flask(__name__)
app.secret_key = 'jonakey'

# henter all dataen fra Pi-en som skal brukes for å sende info fra nettsiden til databasen
db_config = {
    'host': '10.2.3.123',
    'user': 'jonathan',
    'password': 'jonathan2007',
    'database': 'book_store'
}

# Profilsiden
@app.route('/profile/<username>') # Vil tilpasse username med navnet du har logget på med
def profile(username):
    try:
        conn = pymysql.connect(**db_config)
        cur = conn.cursor()

        # Sjekker om brukeren eksisterer
        user_query = "SELECT id, username, email FROM users WHERE username = %s"
        cur.execute(user_query, (username,))
        user = cur.fetchone()
        if not user: 
            flash('Bruker ikke funnet', 'danger')
            return redirect('/')
        # Hvis brukeren ikke eksisterer vil den kjøre denne koden ^
        
        orders_query = "SELECT book_title, order_date FROM orders WHERE user_id = %s"
        cur.execute(orders_query, (user[0],))
        orders = cur.fetchall()

        cur.close()
        conn.close()

        return render_template('profile.html', user=user, orders=orders)
    
    except Exception as e:
        flash(f"Feil med å laste profilen: {e}", 'danger')
        return redirect('/')
    

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
    try:
        conn = pymysql.connect(**db_config)
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            flash('Logget inn! Velkommen {user[1]}', 'success')
            return redirect(url_for('profile', username=user[1]))
        else:
            flash('Ugyldig brukernavn eller passord', 'danger')
            return redirect(url_for('login'))
    except Exception as e:
        flash(f"Feil med innlogging: {e}", 'danger')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        if 'user_id' not in session:
            flash('Logg inn for å legge inn en bestilling', 'danger')
            return redirect(url_for('login'))
        
        book_title = request.form['book_title']
        user_id = session['user_id']

        try:
            conn = pymysql.connect(**db_config)
            cur = conn.cursor()

            query = "INSERT INTO orders (user_id, book_title) VALUES (%s, %s)"
            cur.execute(query, (user_id, book_title))
            conn.commit()

            cur.close()
            conn.close()
            flash('Ordre har blitt bestilt! Tusen takk {user[1]}', 'success')
            return redirect(url_for('profile', username=session['username']))
        except Exception as e:
            flash(f"Feil med bestilling: {e}", 'danger')
            return redirect(url_for('order'))
        
    return render_template('order.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)