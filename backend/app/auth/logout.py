from flask import jsonify, make_response
from . import auth_bp

#logout
@auth_bp.route("logout", methods=["POST"])
def logout():
    body = {
        "message": '',
        "success": True
    }
    response = make_response(jsonify(body))
    return response