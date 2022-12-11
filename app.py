from flask import Flask, render_template, redirect, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

# Configure Flask App
app = Flask(__name__)

# Configure Session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    return render_template("index.html", homeActive = True)

@app.route("/profile")
def profile():
    return render_template("profile.html", profileActive = True)

@app.route("/friends")
def friends():
    return render_template("friends.html", friendsActive = True)

@app.route("/liked")
def liked():
    return render_template("liked.html", likedActive = True)

@app.route("/settings")
def settings():
    return render_template("settings.html", settingsActive = True)

@app.route("/login")
def login():

    session.clear()
    
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/post")
def post():
    return render_template("post.html")

@app.route("/search")
def search():
    return render_template("search.html")
    
