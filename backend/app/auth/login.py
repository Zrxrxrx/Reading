from flask import request
from . import auth_bp
from ..models.user import User
from ..extensions import db
from ..utils.verify import build_jwt, encode_pwd

# Login
@auth_bp.route('login', methods=['POST'])
def login():
    response = {
        'message': '',
        'success': False,
        'token': ''
    }

    data = request.get_json()

    if not data:
        response['message'] = 'no data'
        return response
    
    email = data['email']
    password = data['password']

    # check user if exists
    user = User.query.filter_by(email=email).first()
    if not user:
        response['message'] = 'user does not exist'
        return response
    
    # check user if he/she is blocked
    if user.blocked:
        response['message'] = 'user is blocked, please contact an administrator'
        return response 
    
    # check the password 
    if user.password != password:
        response['message'] = 'password is incorrect'
        user.incorrectTry += 1
        if user.incorrectTry == 10:
            user.blocked = True
        db.session.commit()
        return response

    # success login:
    user.incorrectTry = 0
    db.session.commit()

    response['token'] = build_jwt(user.username, user.id, user.isAdmin, encode_pwd(user.password), user.nameColor)

    response['success'] = True
    return response