from flask import request, g
from app.extensions import db
from . import user_bp

@user_bp.route('editPass',methods=['POST'])
def editPass():
    res = {
        "message": "",
        "success": False
    }

    data = request.get_json()

    # TODO: should verify the old password?
    password = data['password']

    user = g.current_user

    if not user:
        res['message'] = 'user is not exists'
        return res

    # success reset
    user.password = password
    db.session.commit()
    res['success'] = True
    return res