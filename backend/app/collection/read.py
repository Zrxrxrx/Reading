from flask import request, jsonify, g, abort
from datetime import datetime
from ..models.collection import Collection, Book_Collection
from ..models.book import Book
from ..models.rate import Rate
from ..extensions import db
from . import collection_bp


@collection_bp.route('/read/', methods=['POST'])
def add_book_to_read():
    response = {
        'message': 'add book into read fail, ',
        'success': False
    }
    try:
        user = g.current_user
        book_id = request.json.get('bid')

        collection = Collection.query.filter(Collection.id == user.read_collection_id).first()
        book = Book.query.filter(Book.id == book_id).first()

        book.read_counter += 1
        link = Book_Collection(book_id=book_id, collection_id=collection.id,
                               create_at=int(datetime.now().timestamp()))
        link.book = book

        collection.books.append(link)
        db.session.add(link)
        db.session.commit()

        response['message'] = 'add book into read successful'
        response['success'] = True

    except Exception as e:
        response['message'] = response['message'] + str(e)
    return jsonify(response)


@collection_bp.route('/read/', methods=['DELETE'])
def del_book_from_read():
    response = {
        'message': 'del book from read fail, ',
        'success': False
    }
    try:
        user = g.current_user
        book_id = request.json.get('bid')

        link = Book_Collection.query.filter(Book_Collection.book_id == book_id, Book_Collection.collection_id == user.read_collection_id).first()
        link.book.read_counter -= 1
        r = Rate.query.filter(Rate.book == book_id, Rate.user == user.id).first()
        db.session.delete(link)
        db.session.delete(r)
        db.session.commit()
        response['success'] = True
        response['message'] = 'del book from read successfully'
    except Exception as e:
        response['message'] = response['message'] + str(e)
    return jsonify(response)


@collection_bp.route('/isread/', methods=['GET'])
def isread():
    response = {
        'message': 'get isread fail, ',
        'success': False,
        'read': False,
        'rating': 0,
    }
    try:
        user = g.current_user
        book_id = request.args.get('bid')

        link = Book_Collection.query.filter(Book_Collection.book_id == book_id, Book_Collection.collection_id == user.read_collection_id).first()
        r = Rate.query.filter(Rate.book == book_id, Rate.user == user.id).first()
        if link:
            response['read'] = True
            response['rating'] = r.rate if r else 0
        response['message'] = 'get isread successfully'
        response['success'] = True
    except Exception as e:
        response['message'] = response['message'] + str(e)
    return jsonify(response)
