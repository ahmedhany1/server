import sqlite3
from flask import Flask, render_template, redirect, request, url_for
from flask_cors import CORS
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
CORS(app)

connection = sqlite3.connect(":memory:", check_same_thread=False)
cursor = connection.cursor()

cursor.execute("""CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    hash TEXT NOT NULL
)""")
connection.commit()

cursor.execute("""
        CREATE TABLE products (
            id INTEGER PRIMARY_KEY,
            title TEXT,
            price REAL,
            category TEXT,
            img_path TEXT
        )
        """)
connection.commit()

@app.route("/")
def index():
    return render_template("index.html", request_method="GET")

@app.route("/products")
def products():
    """Send products list to client"""
    pass

@app.route("/product/<int:product_id>")
def product(product_id):
    """Send a single product details to client"""
    pass

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        # Extract the username, password and its confirmation
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            flash("Please choose a username")

        # Ensure username does not already exist
        elif len(cursor.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchall()) == 1:
            flash("Username already taken. Please choose a different username.")

        # Ensure password was submitted
        elif not password or not confirmation:
            flash("Please enter a password and confirm it.")

        # Ensure password and confirmation match
        elif password != confirmation:
            flash("Passwords do not match. Please re-enter the passwords and make sure they match")

        else:
            # Insert the new user into the database
            cursor.execute("INSERT INTO users(username, hash) values(?, ?)", (username, generate_password_hash(password)))

            # Log the user in and remember him
            session["user_id"] = cursor.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()[0]

            # Flash message the user upon successful registration
            flash("Registration successful!")

            # Redirect user to home page
            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted
        if not username:
            flash("Username must be provided")

        # Ensure password was submitted
        elif not password:
            flash("Password must be provided")

        # Query database for username
        rows = cursor.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchall()

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0][2], password):
            flash("Invalid username and/or password")

        else:
            # Remember which user has logged in
            session["user_id"] = rows[0][0]

            # Flash message the user if logged in successfully
            flash("You logged in successfully!")

            # Redirect user to home page
            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# @app.post("/postman")
# def postman():
#     request_data = request.get_json()

#     language = None
#     version = None

#     if request_data:
#         if 'language' in request_data:
#             language = request_data['language']
#         if "version_info" in request_data:
#             if "python" in request_data["version_info"]:
#                 version = request_data["version_info"]["python"]

#     return "The language value is: {} v.{}".format(language, version)

