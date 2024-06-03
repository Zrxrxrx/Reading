from flask import request
from ..extensions import db
from . import admin_bp
from ..models.book import Book

# delete book from database
@admin_bp.route('deleteBook', methods=['POST'])
def deleteBook():
    response = {
        'message': '', 
        'success': False
    }

    data = request.get_json()
    if not data:
        response['message'] = 'no data'
        return response

    bid = data['id']

    # check id if is empty
    if id == '':
        response['message'] = 'book id is empty'
        return response

    book = Book.query.filter_by(id=bid).delete()
    db.session.commit()

    response['success'] = True
    return response