from flask import Flask, render_template, request, url_for, redirect
app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path="/")

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

@app.route( '/login')
def login():
   return render_template("login.html")

@app.route( '/register', methods=['GET', 'POST'])
def register():
   msg = ''
   if request.method == 'POST':

      username = request.form['username']
      password = request.form['password']
      email = request.form['email']
      cursor = db.cursor()
      cursor.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", (username, password, email))
      db.commit()
      return redirect(url_for('login'))
      #return "from submitted"
   else:
      return render_template("register.html")

@app.route('/booking/<int:id>')
def booking(id):
   #return f'Booking ID: {id}'
   return render_template("booking.html", bookingid=id)


if __name__ == '__main__':
    app.run (host="127.0.0.1", port=5000, debug=True)