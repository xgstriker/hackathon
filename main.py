from flask import Flask, render_template, request, make_response, redirect, url_for
from models import User
import json
import os
os.environ["TESTING"] = "1"

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        lat = float(request.form.get("lat"))
        lng = float(request.form.get("lng"))

        rlat = 54.6841
        rlng = 25.2860

        if abs(rlat-lat) < 0.01 and abs(rlng-lng) < 0.01:
            return redirect(url_for("login"))
        else:
            return render_template("noaccess.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        import hashlib
        username = request.form.get("username")
        password = hashlib.sha256(request.form.get("password").encode()).hexdigest()
        uid = request.form.get("uid")

        json_data = open("db.json", "r")
        data = json.load(json_data)

        user_name = data['User']['1']['name']
        user_pass = data['User']['1']['password']

        print(username, password, user_name, user_pass)
        if user_pass != password:
            return render_template("noaccess.html")
        elif user_pass == password:
            return redirect(url_for("account"))


@app.route("/account", methods=['GET', 'POST'])
def account():
    if request.method == "GET":
        return render_template("account.html", flat=54.684144, flng=25.285807, name="Bolek")
    elif request.method == "POST":
        lat = request.form.get("lat")
        lng = request.form.get("lng")

        response = render_template("success.html")
        return response


if __name__ == "__main__":
    app.run(debug=True)
