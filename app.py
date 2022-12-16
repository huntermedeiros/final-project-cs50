from flask import Flask, render_template, redirect, url_for, flash, request, session
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

# Configure Database
db = SQL("sqlite:///database.db")


@app.route("/")
def index():
    return render_template("index.html", homeActive = True)

# Users Page Implemented
@app.route("/user/<username>")
@login_required
def user(username):
    # Checks the users info
    userInfo = db.execute("SELECT id, username, name, follower_count, following_count FROM users WHERE username LIKE ?", username)
    if not userInfo:
        flash("User does not exist")
        return redirect("/")
    userPosts = db.execute("SELECT * FROM posts WHERE user_id = ?", userInfo[0]['id'])
    # Checks if this is the users account
    if username == session["username"]:
        isUsersAccount = True
        isFollowing = None
    else:
        isUsersAccount = False
        # If this is not the users account then check if theyre following this account
        if db.execute("SELECT * FROM following WHERE user_id = ? AND follower_id = ?", userInfo[0]['id'], session['user_id']) :
            isFollowing = True
        else:
            isFollowing = False
    return render_template("user.html", userInfo=userInfo[0], userPosts=userPosts, isUsersAccount=isUsersAccount, isFollowing=isFollowing)

# follow implemented
@app.get('/follow/<followed>')
@login_required
def follow(followed):
    # Gets user being followed username and id
    followedInfo = db.execute("SELECT id, username FROM users WHERE username LIKE ?", followed)[0]
    # Check if they are already being followed
    if db.execute("SELECT * FROM following WHERE user_id = ? AND follower_id = ?", followedInfo["id"], session["user_id"]):
        return redirect(url_for("user", username=followedInfo["username"]))
    # Add who has been followed to the following table
    db.execute("INSERT INTO following VALUES (?, ?)", followedInfo["id"], session["user_id"])
    # Updates follower count of user being followed
    db.execute("UPDATE users SET follower_count = follower_count + 1 WHERE id = ?", followedInfo["id"])
    # Updates following count of user following
    db.execute("UPDATE users SET following_count = following_count + 1 WHERE id = ?", session["user_id"])
    return redirect(url_for("user", username=followedInfo["username"]))

# unfollowed implemented
@app.get('/unfollow/<unfollowed>')
@login_required
def unfollow(unfollowed):
    # Gets unfollowed users id and username
    unfollowedInfo = db.execute("SELECT id, username FROM users WHERE username LIKE ?", unfollowed)[0]
    # Check if user is following this account
    if not db.execute("SELECT * FROM following WHERE user_id = ? AND follower_id = ?", unfollowedInfo["id"], session["user_id"]):
        return redirect(url_for("user", username=unfollowedInfo["username"]))
    # Add who has been followed to the following table
    db.execute("DELETE FROM following WHERE user_id = ? AND follower_id = ?", unfollowedInfo["id"], session["user_id"])
    # Updates follower count of user being unfollowed
    db.execute("UPDATE users SET follower_count = follower_count - 1 WHERE id = ?", unfollowedInfo["id"])
    # Updates following count of user unfollowing
    db.execute("UPDATE users SET following_count = following_count - 1 WHERE id = ?", session["user_id"])
    return redirect(url_for("user", username=unfollowedInfo["username"]))

@app.route("/friends")
@login_required
def friends():
    friendsList = db.execute("SELECT username, name FROM users JOIN following ON users.id=following.user_id WHERE follower_id = ?", session["user_id"])
    return render_template("friends.html", friendsActive = True, friendsList=friendsList)

@app.route("/liked")
@login_required
def liked():
    return render_template("liked.html", likedActive = True)

# Implemented Signout
@app.route("/signout")
@login_required
def signout():
    session.clear()
    return redirect("/")

# Implemented Login
@app.post("/login")
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
    session["username"] = username
    return redirect("/")

# Implemented Register
@app.post("/register")
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
    session["username"] = username
    return redirect("/")

@app.route("/post", methods=["GET", "POST"])
@login_required
def post():
    if request.method == "GET":
        return render_template("post.html")
    if request.method == "POST":
        postContent = request.form.get("post-content")
        time = datetime.now().strftime("%y-%m-%d %H:%M:%S")
        db.execute("INSERT INTO posts (user_id, post, date) VALUES (?, ?, ?)", session["user_id"], postContent, time)
        return redirect("/")

@app.route("/search", methods=["GET", "POST"])
def search():
    return render_template("search.html")