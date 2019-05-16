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
            rlat = 54.6996223
            rlng = 25.260032

            if abs(float(rlat)-float(lat)) < 0.001 and abs(float(rlng)-float(lng)) < 0.001:
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

        for x in range(1, 3):
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
    cookies_session_token = request.cookies.get("session_token")
    if cookies_session_token:
        if request.method == "GET":
            json_data = open("test_db.json", "r")
            data = json.load(json_data)

            lats = []
            lngs = []
            locations = []
            positions = []

            json_data = open("test_db.json", "r")
            users_id = json.load(json_data)

            num = users_id['Users']['1']['value']
            #
            # for x in range(1, num):
            #     if users_id['Loc'][f'{x}']['lat'] != "" or users_id['Loc'][f'{x}']['lng'] != "":
            #         lat = data['Loc'][f'{x}']['lat']
            #         lng = data['Loc'][f'{x}']['lng']
            #         locations.append(data['Loc'][f'{x}']['location_name'])
            #         positions.append("{"+f"lat: {lat}, lng: {lng}"+"}")
            username = request.cookies.get("username")
            response = make_response(render_template("account.html", locations=locations, lats=lats, name=username, flat=54.684, lngs=lngs, flng=25.2858, positions=positions))

            return response
        elif request.method == "POST":
            num = int(request.cookies.get("num"))
            lat = request.form.get("lat")
            lng = request.form.get("lng")
            locname = request.form.get("locname")

            loc = Loc(lat, lng, locname, uid)
            Loc.create(loc)

            num += 1

            response = make_response(render_template("success.html"))

            response.set_cookie("num", str(num))
            return response
    else:
        return redirect(url_for("/"))


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
        users_id = json.load(json_data)

        map_id = users_id['Users']['1']['value']

        user = User(name=new_username, password=hashed_password, map_id=map_id)
        User.create(user)

        uid = uID(value=new_uid)
        uID.create(uid)

        Users.edit(obj_id=user_id, value=users)

        response = make_response(redirect(url_for("admin")))

        return response


if __name__ == "__main__":
    app.run(debug=True)
