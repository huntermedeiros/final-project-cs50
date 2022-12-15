from flask import Flask, render_template, redirect, flash, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL
from datetime import datetime

from functions import login_required

# Configure Flask App
app = Flask(__name__)

# Configure Session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///database.db")

@app.route("/")
def index():
    return render_template("index.html", homeActive = True)

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", profileActive = True)

@app.route("/friends")
@login_required
def friends():
    return render_template("friends.html", friendsActive = True)

@app.route("/liked")
@login_required
def liked():
    return render_template("liked.html", likedActive = True)

@app.route("/settings")
@login_required
def settings():
    return render_template("settings.html", settingsActive = True)

@app.route("/signout")
def signout():
    session.clear()
    return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    session.clear()
    username = request.form.get("username")
    password = request.form.get("password")
    if not username:
        flash('Please provide username')
        return redirect("/")
    if not password:
        flash('Please provide password')
        return redirect("/")
    rows = db.execute("SELECT * FROM users WHERE username = ?", username)
    if len(rows) != 1 or not check_password_hash(rows[0]["password_hash"], password):
        flash("Invalid username and/or password")
        return redirect("/")
    session["user_id"] = rows[0]["id"]
    return redirect("/")

@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    name = request.form.get("name")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")
    if not username:
        flash('Please provide username')
        return redirect("/")
    if db.execute("SELECT username FROM users WHERE username LIKE ?", username):
        flash('Username taken')
        return redirect("/")
    if not password:
        flash('Please provide password')
        return redirect("/")
    if not confirmation:
        flash('Please confirm password')
        return redirect("/")
    if confirmation != password:
        flash('Passwords do not match')
        return redirect("/")
    password_hash = generate_password_hash(password)

    currentUser = db.execute("INSERT INTO users (username, name, password_hash) VALUES (?, ?, ?)", username, name, password_hash)
    session["user_id"] = currentUser
    return redirect("/")

@app.route("/post")
@login_required
def post():
    return render_template("post.html")

@app.route("/search", methods=["GET", "POST"])
def search():
    return render_template("search.html")