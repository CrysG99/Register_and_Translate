from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import hashlib

app = Flask(__name__)
app.secret_key = 'jonakey'

app.config['MYSQL_HOST'] = '10.2.3.123'
app.config['MYSQL_USER'] = 'jonathan@localhost'
app.config['MYSQL_PASSWORD'] = 'jonathan2007'
app.config['MYSQL_DB'] = 'book_store'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        try:
            cur = mysql.connection
            cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
            mysql.connection.commit()
            cur.close()
            flash('Registrert! Du kan nå logge inn')
            return redirect(url_for('login'))
        except Exception as e:
            flash('Error: ' + str(e), 'nuh uh')
            return redirect(url_for('register'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, hashed_password))
        user = cur.fetchone()
        cur.close()

        if user:
            flash('Logget inn! Velkommen')
            return redirect(url_for('home'))
        else:
            flash('Ugyldig brukernavn eller passord')
            
    return render_template('login.html')

@app.route('/order')
def order():
    return render_template('order.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)