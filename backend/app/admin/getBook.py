from flask import request
from ..extensions import db
from . import admin_bp
from ..models.book import Book

# Get book by id
@admin_bp.route('getBook', methods=['POST'])
def getBook():
    response = {
        'message': '',
        'success': False,
    }

    data = request.get_json()

    if data == None:
        return response
    bid = data['id']

    # update block status of the user
    book = Book.query.filter_by(id=bid).first()
    response['success'] = True
    response['title'] = book.name
    response['author'] = book.author
    response['edition'] = book.edition
    response['isbn'] = book.isbn
    response['categories'] = book.categories
    response['dop'] = book.dop
    response['cover'] = book.cover
    response['purchase'] = book.purchase
    response['introduction'] = book.introduce
    response['readCount'] = book.read_counter

    return response
