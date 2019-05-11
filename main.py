from flask import Flask, render_template, request, make_response, redirect, url_for
from models import User, Loc, uID
import json
import os

os.environ["GITHUB_CLIENT_ID"] = ""
os.environ["GITHUB_CLIENT_SECRET"] = ""
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "GET":

        response = make_response(render_template("index.html"))
        return response
    elif request.method == "POST":
        lat = request.form.get("lat")
        lng = request.form.get("lng")

        if lat == "" or lng == "":
            return redirect(url_for("login"))
        else:
            rlat = 54.6841
            rlng = 25.2860

            if abs(rlat-lat) < 0.1 and abs(rlng-lng) < 0.1:
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

        value_data = open("test_db.json", "r")
        value = json.load(value_data)

        json_data = open("db.json", "r")
        data = json.load(json_data)
        print(data)

        if data['User']['1']['password'] == password and value["uID"]['1']['value'] == uid:
            response = redirect(url_for("account"))

            num = 1
            response.set_cookie("username", username)
            response.set_cookie("num", str(num))
            return response

        elif data['User']['2']['password'] == password and value["uID"]['2']['value'] == uid:
            response = redirect(url_for("account"))

            num = 1
            response.set_cookie("username", username)
            response.set_cookie("num", str(num))
            return response
        else:
            return render_template("noaccess.html")


@app.route("/account", methods=['GET', 'POST'])
def account():
        if request.method == "GET":
            json_data = open("test_db.json", "r")
            data = json.load(json_data)

            lats = []
            lngs = []
            locations = []
            positions = []
            num = int(request.cookies.get('num'))
            for x in range(1, num):
                if data['Loc'][f'{x}']['lat'] != "" or data['Loc'][f'{x}']['lng'] != "":
                    lat = data['Loc'][f'{x}']['lat']
                    lng = data['Loc'][f'{x}']['lng']
                    locations.append(data['Loc'][f'{x}']['locname'])
                    positions.append("{"+f"lat: {lat}, lng: {lng}"+"}")
            username = request.cookies.get("username")
            response = make_response(render_template("account.html", locations=locations, lats=lats, name=username, flat=54.6841, lngs=lngs, flng=25.2858, positions=positions))

            return response
        elif request.method == "POST":
            lat = request.form.get("lat")
            lng = request.form.get("lng")
            locname = request.form.get("locname")
            num = int(request.cookies.get("num"))

            loc = Loc(lat, lng, locname)
            Loc.create(loc)

            num += 1
            response = render_template("success.html")

            response.set_cookie("num", str(num))
            return render_template("success.html")


@app.route("/admin", methods=['GET', 'POST'])
def admin():
    if request.method == "GET":
        username = request.cookies.get("username")

        response = make_response(render_template("admin.html", name=username))
        return response
    if request.method == "POST":
        new_uid = request.form.get("uid")
        new_username = request.form.get("username")
        new_password = request.form.get("password")

        user = User(name=new_username, password=new_password)
        User.create(user)

        uid = uID(value=new_uid)
        uID.create(uid)

        response = make_response(redirect(url_for("admin")))

        return response


if __name__ == "__main__":
    app.run(debug=True)
