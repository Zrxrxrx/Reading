from flask import make_response, request
from ..extensions import db
from . import auth_bp
from ..models.user import User


# when user forget password, send OTP to user email address
# after verify OTP, user can reset password
@auth_bp.route('/resetVerify', methods=['POST'])
def reset_verfify():
    # TODO: hard coding, waiting email feature done
    response = {
        'message': '', 
        'success': True
    }
    return response
   
@auth_bp.route('resetPass',methods=['POST'])
def reset():
    res = {
        "message": "",
        "success": False
    }

    data = request.get_json()

    email = data['email']
    password = data['password']
    code = data['code']

    if code != '123456':
        res['message'] = 'code is incorrect'
        return res
    
    user = User.query.filter_by(email=email).first()

    if not user:
        res['message'] = 'user is not exists'
        return res    

    # success reset
    user.password = password
    db.session.commit()
    res['success'] = True
    return res