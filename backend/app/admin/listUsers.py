from flask import request
from ..extensions import db
from . import admin_bp
from ..models.user import User

# List all users from database
@admin_bp.route('listUsers', methods=['GET'])
def listUsers():
    response = {
        'users': '', 
        'success': False
    }

    data = [{ "name": user.username, "nameColor": user.nameColor, "email": user.email, "id": user.id, "blocked": user.blocked } for user in User.query.all()]
    response['success'] = True
    response['users'] = data

    return response