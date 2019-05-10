from flask import Flask, render_template, request, make_response, redirect, url_for
from models import User

import uuid
import hashlib
app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        hashed_password = hashlib.sha256(password)
    
if __name__ == "__main__":
    app.run(debug=True)
