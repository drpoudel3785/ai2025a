from flask import Flask, render_template, request, redirect, url_for, session, make_response
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path="/")

#https://myaccount.google.com/apppasswords
# Mail Config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'dharmarajpoudel@gmail.com'
app.config['MAIL_PASSWORD'] = 'murwxywnyjwhsvso'
app.config['MAIL_DEFAULT_SENDER'] = 'dharmarajpoudel@gmail.com'
mail = Mail(app)

# Secret Key
app.secret_key = 'secret123'
# Token generator
serializer = URLSafeTimedSerializer(app.secret_key)

import mysql.connector
# 1. Connect
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="P@ssw0rd",
    database="ai2025a",
    port=3307
)

@app.route( '/')
def index():
   return render_template("index.html")

@app.route( '/about')
def about():
    return render_template("about.html")

@app.route( '/contact')
def contact():
   return render_template("contact.html")

# @app.route( '/login')
# def login():
#    return render_template("login.html")
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM users WHERE username = %s AND status=%s", 
            (username, 1)
        )
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):
            # SESSION
            session['loggedin'] = True
            session['id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']

            # ROLE BASED REDIRECT
            if user['role'] == 'admin':
                redirect_url = url_for('admin_dashboard')
            else:
                redirect_url = url_for('user_dashboard')

            # COOKIE
            response = make_response(redirect(redirect_url))
            response.set_cookie('username', user['username'], max_age=60*60*24*15)
            response.set_cookie('password', password, max_age=60*60*24*15)

            return response
        else:
            msg = 'Invalid username or password'

    return render_template("login.html", msg=msg)

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'loggedin' in session and session['role'] == 'admin':
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id, username, email, role, status FROM users")
        users = cursor.fetchall()
        total_users = len(users)   # COUNT USERS
        return render_template('admin/admin_dashboard.html', users=users,  total_users=total_users)
    

    return redirect(url_for('login'))


@app.route('/user/dashboard')
def user_dashboard():
    if 'loggedin' in session and session['role'] == 'user':
        return render_template('user/user_dashboard.html')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    response = make_response(redirect(url_for('login')))
    response.delete_cookie('username')
    return response

# @app.route( '/register', methods=['GET', 'POST'])
# def register():
#    msg = ''
#    if request.method == 'POST':

#       username = request.form['username']
#       password = request.form['password']
#       email = request.form['email']
#       cursor = db.cursor()
#       cursor.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", (username, password, email))
#       db.commit()
#       return redirect(url_for('login'))
#       #return "from submitted"
#    else:
#       return render_template("register.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        cursor = db.cursor()

        # Check existing user
        cursor.execute("SELECT * FROM users WHERE email=%s OR username=%s", (email, username))
        account = cursor.fetchone()

        if account:
            return 'Account already exists!'
        else:
            hashed_password = generate_password_hash(password)

            cursor.execute(
                "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
                (username, hashed_password, email)
            )
            db.commit()

            # Generate activation token
            token = serializer.dumps(email, salt='email-confirm')
            link = f"http://localhost:5000/activate/{token}"

            email_msg = Message(
                'Activate Your Account',
                recipients=[email]
            )
            email_msg.body = f'Click the link to activate your account:\n{link}'
            mail.send(email_msg)

            return 'Registration successful! Check your email.'

    return render_template("register.html")


@app.route('/activate/<token>')
def activate(token):
   try:
      email = serializer.loads(token, salt='email-confirm', max_age=3600)
   except:
      return "Activation link expired"
   cursor = db.cursor()
   cursor.execute("UPDATE users SET status=1, role='user'  WHERE email=%s", (email,))
   db.commit()
   cursor.close()
   return "Account activated successfully!"

@app.route('/booking/<int:id>')
def booking(id):
   #return f'Booking ID: {id}'
   return render_template("booking.html", bookingid=id)

#CRUD
@app.route('/admin/add_user', methods=['GET', 'POST'])
def add_user():
    if 'loggedin' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        role = request.form['role']
        password = generate_password_hash(request.form['password'])
        status=1

        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO users (username, email, password, role, status) VALUES (%s, %s, %s, %s, %s)",
            (username, email, password, role, status)
        )
        db.commit()

        return redirect(url_for('admin_dashboard'))

    return render_template('admin/add_user.html')
@app.route('/admin/edit_user/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    if 'loggedin' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))

    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        role = request.form['role']
        status = request.form['status']

        cursor.execute(
            "UPDATE users SET username=%s, email=%s, role=%s, status=%s WHERE id=%s",
            (username, email, role, status, id)
        )
        db.commit()
        return redirect(url_for('admin/admin_dashboard'))

    cursor.execute("SELECT * FROM users WHERE id=%s", (id,))
    user = cursor.fetchone()
    return render_template('admin/edit_user.html', user=user)
@app.route('/admin/delete_user/<int:id>')
def delete_user(id):
    if 'loggedin' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))

    cursor = db.cursor()
    cursor.execute("DELETE FROM users WHERE id=%s", (id,))
    db.commit()

    return redirect(url_for('admin/admin_dashboard'))


if __name__ == '__main__':
    app.run (host="127.0.0.1", port=5000, debug=True)