from flask import Flask, render_template, request, make_response, redirect, url_for
from models import User, Loc, uID, Users
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
        num = 1
        response = make_response(render_template("index.html"))
        response.set_cookie("num", str(num))
        return response
    elif request.method == "POST":
        lat = request.form.get("lat")
        lng = request.form.get("lng")

        print(lat, lng)

        if lat == "" or lng == "":
            return redirect(url_for("login"))
        else:
            rlat = 54.6826067
            rlng = 25.2833527

            if abs(float(rlat)-float(lat)) < 0.01 and abs(float(rlng)-float(lng)) < 0.01:
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

        num = value['Users']['1']['value'] + 1

        for x in range(1, num):
            if value['User'][f"{x}"]['name'] == username and value['User'][f"{x}"]['password'] == password and value["uID"][f"{x}"]['value'] == uid:
                response = redirect(url_for("account"))

                date = datetime.now() + timedelta(minutes=1)
                session_token = uuid.uuid4()

                response.set_cookie("username", username, expires=date)
                response.set_cookie("session_token", str(session_token), expires=date)
                response.set_cookie("position", str(x))
                return response

        return render_template("noaccess.html")


@app.route("/account", methods=['GET', 'POST'])
def account():
        if request.method == "GET":
            pos = int(request.cookies.get('position'))

            lats = []
            lngs = []
            locations = []
            positions = []

            json_data = open("test_db.json", "r")
            data = json.load(json_data)

            users_id = data['Users']["1"]['value']

            map_sum = int(data['User'][f"1"]['map_id']) + 1

            if (users_id > 1):
                for x in range(2, users_id):
                    map_sum += int(data['User'][f"{x}"]['map_id'])

            print(data['Loc'][f"{pos}"]['uid'], "\n", data['User'][f"{pos}"]['name'])
            for x in range(1, map_sum):
                if data['Loc'][f"{x}"]['lat'] != "" and data['Loc'][f"{x}"]['lng'] != "" and data['Loc'][f"{x}"]['uid'] == data['User'][f"{pos}"]['name']:
                    lat = data['Loc'][f'{x}']['lat']
                    lng = data['Loc'][f'{x}']['lng']
                    locations.append(data['Loc'][f'{x}']['location_name'])
                    positions.append("{"+f"lat: {lat}, lng: {lng}"+"}")
            username = request.cookies.get("username")
            response = make_response(render_template("account.html", locations=locations, lats=lats, name=username, flat=54.684, lngs=lngs, flng=25.2858, positions=positions))

            return response
        elif request.method == "POST":
            pos = request.cookies.get("position")
            lat = request.form.get("lat")
            lng = request.form.get("lng")
            locname = request.form.get("locname")

            json_data = open("test_db.json", "r")
            data = json.load(json_data)

            id = data['User'][f"{pos}"]['name']

            loc = Loc(lat, lng, locname, id)
            Loc.create(loc)

            num = data['User'][f"{pos}"]['map_id']

            num += 1

            User.edit(obj_id=pos, map_id=num)

            response = make_response(render_template("success.html"))

            response.set_cookie("num", str(num))
            return response


@app.route("/admin", methods=['GET', 'POST'])
def admin():
    if request.method == "GET":
        username = request.cookies.get("username")

        response = make_response(render_template("admin.html", name=username))
        return response
    if request.method == "POST":
        import hashlib
        new_uid = request.form.get("uid")
        new_username = request.form.get("username")
        new_password = request.form.get("password")

        hashed_password = hashlib.sha256(new_password.encode()).hexdigest()

        json_data = open("test_db.json", "r")
        data = json.load(json_data)

        users_value = data['Users']['1']['value']

        user = User(name=new_username, password=hashed_password, map_id=1)
        User.create(user)

        uid = uID(value=new_uid)
        uID.create(uid)

        users_value += 1

        user_id = 1

        Users.edit(obj_id=user_id, value=users_value)

        response = make_response(redirect(url_for("admin")))

        return response


if __name__ == "__main__":
    app.run(debug=True)
