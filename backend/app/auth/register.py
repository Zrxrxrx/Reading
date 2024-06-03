from flask import request
from ..extensions import db
from . import auth_bp
from ..models.user import User
from ..models.collection import Collection
from datetime import datetime

@auth_bp.route('register', methods=['POST'])
def register():
    response = {
        'message': '', 
        'success': False
    }

    data = request.get_json()
    if not data:
        response['message'] = 'no data'
        return response

    username = data['username']
    password = data['password']
    email = data['email']

    # check username if is empty
    if username == '':
        response['message'] = 'username is empty'
        return response

    # check password length
    if len(password) < 8:
        response['message'] = 'password is too short'
        return response

    # check if user exists
    temp_user = User.query.filter_by(email=email).first()
    if temp_user:
        response['message'] = 'user exists'
        return response

    # add new record into user table
    user = User(username=username, password=password, email=email, registerDate=datetime.now().timestamp())
    __create_collection(user)
    db.session.add(user)
    db.session.commit()

    response['success'] = True
    return response

# create two collections for the user
# 1.main collection: can not be deleted
# 2.have read collection: can not be deleted
def __create_collection(user):
    main_collection = Collection(name='main', description='Default Collection', deleteable=False)
    haveRead = Collection(name='Have Read', description='The books you have read.', deleteable=False, isRead=True)
    user.collections.append(main_collection)
    user.collections.append(haveRead)
    main_collection.users.append(user)
    haveRead.users.append(user)
    db.session.add(main_collection, haveRead)
    db.session.flush()
    user.read_collection_id = haveRead.id
