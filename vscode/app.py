from flask import Flask, render_template
app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path="/")

@app.route( '/')
def index():
   return render_template("index.html")

@app.route( '/about')
def about():
    return render_template("about.html")

@app.route( '/contact')
def contact():
   return render_template("contact.html")

@app.route('/booking/<int:id>')
def booking(id):
   #return f'Booking ID: {id}'
   return render_template("booking.html", bookingid=id)


if __name__ == '__main__':
    app.run (host="127.0.0.1", port=5000, debug=True)