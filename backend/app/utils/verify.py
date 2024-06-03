from flask import request, g, abort
from hashlib import md5
from ..models.user import User
from ..user import user_bp
from ..admin import admin_bp
from ..book import bookapi
from ..collection import collection_bp
from ..rate import rate_bp

import jwt

JWT_SECRET_KEY = 'COMP3900_W14B_NULL'


@user_bp.before_request
@admin_bp.before_request
@bookapi.before_request
@collection_bp.before_request
@rate_bp.before_request
def verify_token():
    token = request.headers.get("Authorization")
    if not token:
        print('token is empty ')
        abort(401)
    print('token is: ' + token)

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms="HS256")
    except Exception:
        print("token is invalid")
        g.current_user = None
        abort(403)

    uid = payload['uid']
    pwHash = payload['pwHash']
    user = User.query.filter_by(id=uid).first()
    if not user:
        abort(403)
        pass

    if encode_pwd(user.password) != pwHash:
        print(f"user: {user.username} password was changed")
        g.current_user = None
        abort(403)

    g.current_user = user

def build_jwt(username, uid, isAdmin, pwHash, nameColor="black"):
    payload_data = {
        "uid": uid,
        "username": username,
        "nameColor": nameColor,
        "isAdmin": isAdmin,
        "pwHash": pwHash
    }

    return jwt.encode(payload_data, JWT_SECRET_KEY, algorithm="HS256")


def encode_pwd(pwd: str):
    return md5(pwd.encode(encoding='UTF-8')).hexdigest()
