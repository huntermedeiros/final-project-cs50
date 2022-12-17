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
    friendsposts = None
    # Checks if user is logged in
    if not session.get("user_id") is None:
        friendsposts = db.execute("SELECT username, name, post, date FROM posts JOIN users ON users.id=posts.user_id JOIN following ON following.user_id=posts.user_id WHERE follower_id = ? ORDER BY date DESC", session["user_id"])
    return render_template("index.html", friendsposts=friendsposts, homeActive = True, )

@app.route("/user/<username>")
@login_required
def user(username):
    # Checks the users info
    userInfo = db.execute("SELECT id, username, name, follower_count, following_count FROM users WHERE username LIKE ?", username)
    # Checks if user exists
    if not userInfo:
        flash("User does not exist")
        return redirect("/")
    userPosts = db.execute("SELECT * FROM posts WHERE user_id = ? ORDER BY date DESC", userInfo[0]['id'])
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
    # Grabs a list of the people the user follows
    friendsList = db.execute("SELECT username, name, follower_count, following_count FROM users JOIN following ON users.id=following.user_id WHERE follower_id = ?", session["user_id"])
    return render_template("friends.html", friendsActive = True, friendsList=friendsList)

@app.route("/signout")
@login_required
def signout():
    # Clears session
    session.clear()
    return redirect("/")

@app.post("/login")
def login():
    session.clear()
    # Gets username and password from form
    username = request.form.get("username")
    password = request.form.get("password")
    # Checks if username was given
    if not username:
        flash('Please provide username')
        return redirect("/")
    # Checks if password was given
    if not password:
        flash('Please provide password')
        return redirect("/")
    # Gets info on user from database
    rows = db.execute("SELECT * FROM users WHERE username = ?", username)
    # Checks if that user exists and if the password hash matches
    if len(rows) != 1 or not check_password_hash(rows[0]["password_hash"], password):
        flash("Invalid username and/or password")
        return redirect("/")
    # If complete the user is logged in and their info is stored to session
    session["user_id"] = rows[0]["id"]
    session["username"] = username
    session["name"] = rows[0]['name']
    return redirect("/")

@app.post("/register")
def register():
    # Stores username, name, passwords, and confirmation
    username = request.form.get("username")
    name = request.form.get("name")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")
    # Checks if username has been inputed
    if not username:
        flash('Please provide username')
        return redirect("/")
    # Checks if the username has already been taken
    if db.execute("SELECT username FROM users WHERE username LIKE ?", username):
        flash('Username taken')
        return redirect("/")
    # Checks if password is there
    if not password:
        flash('Please provide password')
        return redirect("/")
    # Checks if confirmation is there
    if not confirmation:
        flash('Please confirm password')
        return redirect("/")
    # Checks if the confirmation matches the password
    if confirmation != password:
        flash('Passwords do not match')
        return redirect("/")
    password_hash = generate_password_hash(password)

    currentUser = db.execute("INSERT INTO users (username, name, password_hash) VALUES (?, ?, ?)", username, name, password_hash)
    # Stores id of user, username, and name of the current user
    session["user_id"] = currentUser
    session["username"] = username
    session["name"] = name
    return redirect("/")

@app.route("/post", methods=["GET", "POST"])
@login_required
def post():
    if request.method == "GET":
        return render_template("post.html")
    if request.method == "POST":
        # Gets what the user has posted
        postContent = request.form.get("post-content")
        # If there is no content to post flash user with error
        if not postContent:
            flash("Please put something to post")
            redirect("/post")
        # Grabs time that the user made post
        time = datetime.now().strftime("%y-%m-%d %H:%M")
        # Add post to database
        db.execute("INSERT INTO posts (user_id, post, date) VALUES (?, ?, ?)", session["user_id"], postContent, time)
        return redirect("/")

@app.route("/search")
def search():
    # Gets the arguments from the search bar
    search = request.args.get("search")
    # Searches for all users that match the criteria of the search
    resultsUsers = db.execute("SELECT username, name, follower_count, following_count FROM users WHERE username LIKE ? OR name LIKE ?", "%" + search + "%", "%" + search + "%")
    # Searches for all of the posts that contain the criteria
    resultsPosts = db.execute("SELECT username, name, post, date FROM posts JOIN users ON users.id=posts.user_id WHERE post LIKE ? ORDER BY date DESC", "%" + search + "%" )
    return render_template("search.html", resultsUsers=resultsUsers, resultsPosts=resultsPosts)