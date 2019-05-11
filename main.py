from flask import Flask, render_template, request, make_response, redirect, url_for
from models import User, Loc
from _datetime import datetime, timedelta
import ast
import uuid, hashlib
import json
import os
os.environ["TESTING"] = "1"

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template("index.html", https=True)
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
            response = redirect(url_for("account"))

            date = datetime.now() + timedelta(minutes=1)
            session_token = uuid.uuid4()

            response.set_cookie("username", user_name, expires=date)
            response.set_cookie("session_token", str(session_token), expires=date)
            return response


@app.route("/account", methods=['GET', 'POST'])
def account():
    cookies_session_token = request.cookies.get("session_token")
    if cookies_session_token:
        if request.method == "GET":
        #     location = request.cookies.get("locations")
        #
        #     location = ast.literal_eval(location)
        #     locations = location["locname"]

            json_data = open("test_db.json", "r")
            data = json.load(json_data)

            num = request.cookies.get("num")

            lats = []
            lngs = []
            locations = []
            positions = []
            for x in range(1, int(num)):
                lats.append(data['Loc'][f'{x}']['lat'])
                lngs.append(data['Loc'][f'{x}']['lng'])
                lat = data['Loc'][f'{x}']['lat']
                lng = data['Loc'][f'{x}']['lng']
                locations.append(data['Loc'][f'{x}']['locname'])
                positions.append("{"+f"lat: {lat}, lng: {lng}"+"}")
            response = make_response(render_template("account.html", locations=locations, lats=lats, flat=54.684144, lngs=lngs, flng=25.285807, positions=positions,  name="Bolek"))

            return response
        elif request.method == "POST":
            num = int(request.cookies.get("num"))
            lat = request.form.get("lat")
            lng = request.form.get("lng")
            locname = request.form.get("locname")

            # locations = {"lat": [""], "lng": [""], "locname": []}
            # locations["lat"].append(lat)
            # locations["lng"].append(lng)
            # locations["locname"].append(locname)

            loc = Loc(lat, lng, locname)
            Loc.create(loc)

            num += 1

            response = make_response(render_template("success.html"))

            response.set_cookie("num", str(num))
            return response
    else:
        return redirect(url_for("/"))


if __name__ == "__main__":
    app.run(debug=True)
