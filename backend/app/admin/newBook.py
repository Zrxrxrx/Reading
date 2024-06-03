from flask import request
from ..extensions import db
from . import admin_bp
from ..models.book import Book, Book_Tag
from ..models.user import *

# crate new book, and add new record to book table and book_tag table
@admin_bp.route('newBook', methods=['POST'])
def newBook():
    response = {
        'message': '', 
        'success': False
    }

    data = request.get_json()
    if not data:
        response['message'] = 'no data'
        return response
    
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

    book = Book(name=name, author=author, edition=edition, isbn=isbn, categories=categories, introduce=introduction, dop=dop, purchase=purchase, cover=cover)
    db.session.add(book)
    db.session.commit()
    db.session.flush()
    for x in categories.split(";"):
        checkTag = Tag.query.filter(Tag.name == x).first()
        if not checkTag:
            tag = Tag(name=x)
            db.session.add(tag)
            db.session.commit()
            db.session.flush()
            link = Book_Tag(book_id=book.id, tag_id=tag.id)
            db.session.add(link)
        else:
            link = Book_Tag(book_id=book.id, tag_id=checkTag.id)
            db.session.add(link)

    db.session.commit()

    response['success'] = True
    return response