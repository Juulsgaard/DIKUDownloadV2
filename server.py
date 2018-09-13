import json

import jwt
from flask import Flask, request

from lib.canvas_session import CanvasSession
from lib.encryption import AESCipher

jwt_secret = "Not very secret"
login_secret = "Not very secret!"

app = Flask(__name__)


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    try:
        session = CanvasSession(username, password).session
    except:
        return "Bad login"

    token = session.cookies.get_dict()["canvas_session"]
    cipher = AESCipher(login_secret)

    username_enc = cipher.encrypt(username)
    password_enc = cipher.encrypt(password)

    jwt_token = jwt.encode({"usr": username_enc, "psw": password_enc, "tkn": token}, jwt_secret)

    return jwt_token


@app.route("/calendar/today")
def calendar_today():
    return


@app.route("/test", methods=["POST"])
def test():
    session = get_session()
    courses = session.api_call("/courses")
    return json.dumps(courses)


def get_user():
    jwt_token = request.headers["Auth"]
    user = jwt.decode(jwt_token, jwt_secret)
    cipher = AESCipher(login_secret)

    return {
        "username": cipher.decrypt(user["usr"]),
        "password": cipher.decrypt(user["psw"]),
        "token": user["tkn"]
    }


def get_session():
    user = get_user()
    return CanvasSession(**user)
