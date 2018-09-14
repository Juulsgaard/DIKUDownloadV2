import jwt
from flask import Blueprint, request

from lib.canvas_session import CanvasSession
from lib.encryption import AESCipher
from server.tools import login_secret, jwt_secret

bp = Blueprint('authentication', __name__)


@bp.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    try:
        session = CanvasSession(username, password).get_session()
    except:
        return "Bad login"

    token = session.cookies.get_dict()["canvas_session"]
    cipher = AESCipher(login_secret)

    username_enc = cipher.encrypt(username)
    password_enc = cipher.encrypt(password)

    jwt_token = jwt.encode({"usr": username_enc, "psw": password_enc, "tkn": token}, jwt_secret)

    return jwt_token
