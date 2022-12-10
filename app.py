from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/friends")
def friends():
    return render_template("friends.html")

@app.route("/liked")
def liked():
    return render_template("liked.html")



    