from flask import request
from ..extensions import db
from . import admin_bp
from ..models.book import Book

# Edit book
@admin_bp.route('editBook', methods=['POST'])
def editBook():
    response = {
        'message': '', 
        'success': False
    }

    data = request.get_json()
    if not data:
        response['message'] = 'no data'
        return response

    bid = data['id']
    name = data['title']
    author = data['author']
    edition = data['edition']
    isbn = data['isbn']
    dop = data['dop']
    categories = data['categories']
    purchase = data['purchase']
    cover = data['cover']
    introduction = data['introduction']
 
    # check id if is empty
    if id == '':
        response['message'] = 'book id is empty'
        return response

    # check book name if is empty
    if name == '':
        response['message'] = 'book name is empty'
        return response

    # check author name if is empty
    if author == '':
        response['message'] = 'author name is empty'
        return response

    # check edition if is empty
    if edition == '':
        response['message'] = 'edition is empty'
        return response

    # check isbn if is empty
    if isbn == '':
        response['message'] = 'isbn is empty'
        return response

    # check dop if is empty
    if dop == '':
        response['message'] = 'date of publication is empty'
        return response

    # check categories if is empty
    if categories == '':
        response['message'] = 'categories is empty'
        return response

    # check introduction if is empty
    if introduction == '':
        response['message'] = 'introduction is empty'
        return response

    book = Book.query.filter_by(id=bid).first()
    book.name = name
    book.author = author
    book.edition = edition
    book.isbn = isbn
    book.dop = dop
    book.categories = categories
    book.purchase = purchase
    book.cover = cover
    book.introduce = introduction
    db.session.commit()

    response['success'] = True
    return response