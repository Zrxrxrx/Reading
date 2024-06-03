from flask import request
from ..extensions import db
from . import admin_bp
from ..models.user import User

# blocking a user, so that he can't login anymore
@admin_bp.route('blockUser', methods=['POST'])
def blockUser():
    response = {
        'message': '',
        'username': '',
        'blocked': False,
        'success': False
    }

    data = request.get_json()

    if data == None:
        return response
    uid = data['uid']
    block = data['block']
    if block == "true":
        block = True
    elif block == "false":
        block = False

    # update block status of the user
    user = User.query.filter_by(id=uid).first()
    user.blocked = block
    db.session.commit()
    response['success'] = True
    response['username'] = user.username
    response['blocked'] = user.blocked
    if user.blocked is True:
        response['message'] = 'User is blocked'
    elif user.blocked is False:
        response['message'] = 'User is unblocked'

    return response