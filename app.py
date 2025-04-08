from cs50 import SQL
from datetime import datetime
import bleach
from flask import Flask, render_template, request, session, redirect
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required

app = Flask(__name__)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Setting up Years
YEARS = [
    "2024",
    "2023",
    "2022",
    "2021",
    "<2021"
]

DURATION = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    ">6"
]


@app.route("/")
def index():
    rating = db.execute("SELECT quality FROM reviews")
    sum = 0
    table = []
    ranks = [0,0,0,0,0]
    table_ranks = ["Awesome", "Great", "Good", "Fine", "Bad"]
    size = len(rating)
    for row in rating:
        sum += row["quality"]
    avg_rate = "{:.2f}".format(sum / size)

    # To display the user's review on the index page in decending time order
    reviews = db.execute("SELECT * FROM reviews ORDER BY time DESC;")


    # To display the rating table on the index page
    quality = db.execute("SELECT quality FROM reviews")
    # Add the ranks in a list
    for rating in quality:
        ranks[rating["quality"] - 1] += 1
    # Sorting list from biggest to smallest
    reverse_ranks = ranks[::-1]

    for value1, value2 in zip(table_ranks, reverse_ranks):
        table.append({"label": value1, "value": value2})

    return render_template("index.html", avg_rate=avg_rate, size=size, reviews=reviews, table=table)


@app.route("/review", methods=["POST", "GET"])
@login_required
def review(error_mes=None):
    if not error_mes:
        return render_template("review.html", years=YEARS, durations=DURATION)
    else:
        return render_template("review.html", years=YEARS, durations=DURATION, error=error_mes)

@app.route("/submit", methods=["POST", "GET"])
@login_required
def submit():
    # Creata a new tables to keep track of user's purchase history
    '''
    CREATE TABLE reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        year TEXT,
        duration TEXT,
        workload INTEGER,
        usefulness INTEGER,
        quality INTEGER,
        time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    );
    '''

    # Submit via post method
    if request.method == ("POST"):
        rows = db.execute("SELECT * FROM reviews WHERE user_id = ?", session["user_id"])
        if len(rows) > 0:
            return review("You have already added a review")

        year = request.form.get("year")
        duration = request.form.get("duration")
        workload = request.form.get("workload")
        usefulness = request.form.get("usefulness")
        quality = request.form.get("quality")
        comment = bleach.clean(request.form.get("comment"))

        # Ensure the elements are not empty
        if not (year and duration and workload and usefulness and quality and comment):
            return review("Empty Box")

        # Ensure the years selected is in within the list
        if year not in YEARS:
            return review("Invalid Year")

        # Ensure the years selected is in within the list
        elif duration not in DURATION:
            return review("Invalid Duration")

        # Ensure the worload, usefulness, quality is within
        try:
            workload = int(workload)
            usefulness = int(usefulness)
            quality = int(quality)
        except ValueError:
            return review("Invalid rating")
        if not (1 <= workload <= 5 and 1 <= usefulness <= 5 and 1 <= quality <= 5):
            return review("Invalid rating")

        #Store the user's review
        db.execute("INSERT INTO reviews (user_id, year, duration, workload, usefulness, quality, comment, time) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    session["user_id"], year, duration, workload, usefulness, quality, comment, datetime.now())
        return index()
    else:
        return review()


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/account")
@login_required
def account():
    return render_template("account.html")


@app.route("/school", methods=["POST", "GET"])
@login_required
def school():
    if request.method == ("POST"):
        school = request.form.get("school")
        if not school:
            return render_template("account.html", error = "Invalid School")
        else:
            # Insert school into Database:
            db.execute("UPDATE users SET school = ? WHERE id = ?", school, session["user_id"])
            # Update the session varaible
            rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
            session["school"] = rows[0]["school"]
            return render_template("account.html")
    else:
        return render_template("account.html")


@app.route("/password", methods=["POST", "GET"])
@login_required
def password():
    if request.method == ("POST"):
        if not (request.form.get("old_password") or request.form.get("new_password") or request.form.get("renew_password")):
            return render_template("account.html", error="Empty Passwords")

        # Setting up the password's variable
        old_pw = request.form.get("old_password")
        new_pw = request.form.get("new_password")
        renew_pw = request.form.get("renew_password")

        # Hashed password selected from db
        password_db = db.execute("SELECT * FROM users WHERE id = ?",session["user_id"])[0]["hash"]

        if check_password_hash(password_db, old_pw):

            if new_pw == renew_pw:
                # Generate a new hashed password
                hashed_pw = generate_password_hash(new_pw)
                # Update the password
                db.execute("UPDATE users SET hash = ? WHERE id = ?", hashed_pw, session["user_id"])
                return render_template("account.html", success="Successful!")
            else:
                print(f"new_pw: {new_pw}, renew_pw: {renew_pw}")  # Debugging line
    else:
        return render_template("account.html")


# This code is adjusted from the PS9: Finance
@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    # User reached route via Post
    if request.method == ("POST"):
        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("login.html", error = "Invalid username and/or password")
        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("login.html", error = "Invalid username and/or password")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return render_template("login.html", error = "Invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]
        session["school"] = rows[0]["school"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via Get
    else:
        return render_template("login.html")


# This code is adjusted from the PS9: Finance
@app.route("/logout")
def logout():
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

# This code is adjusted from the PS9: Finance
@app.route("/register", methods=["GET", "POST"])
def register():
    """
    CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    hash TEXT NOT NULL,
    school TEXT);
    """
    if request.method == "POST":
        # Check for username:
        username = request.form.get("username")
        if not username:
            return render_template("register.html", error = "Username is empty")

        # Check if Username Exists:
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) > 0:
            return render_template("register.html", error = "Username is already taken")

        # Get and Validate Password:
        userpassword = request.form.get("password")
        con_userpassword = request.form.get("confirmation")
        if not userpassword or not con_userpassword:
            return render_template("register.html", error = "Re-enter password empty")
        elif userpassword != con_userpassword:
            return render_template("register.html", error = "passwords do not match")

        # Hash the Password
        hashed_password = generate_password_hash(userpassword)

        # Insert User into Database:
        db.execute("INSERT INTO users (username, hash) VALUES(?,?)", username, hashed_password)

        # Redirect to Login:
        return render_template("login.html", success="Account Created!")

    # User reached via GET
    else:
        return render_template("register.html")
