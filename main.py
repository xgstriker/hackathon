from flask import Flask, render_template, request, make_response, redirect, url_for
from models import User

import uuid, hashlib
app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return redirect(url_for("login"))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        print("hello")
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        hashed_pass = hashlib.sha256(password.encode()).hexdigest()

        user = User(name=username, password=hashed_pass)
        User.create(user)
        User.edit(obj_id=user.id)

        return redirect(url_for("account"))


@app.route("/account", methods=['GET', 'POST'])
def account():
    if request.method == "GET":
        return render_template("account.html", lat=54.684144, lng=25.285807)
    elif request.method == "POST":

        response = render_template("success.html")

        return response


if __name__ == "__main__":
    app.run(debug=True)
