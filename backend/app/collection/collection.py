from flask import request, jsonify, g, abort
from datetime import datetime
from ..models.collection import Collection, Book_Collection, ReaderGroup
from ..models.book import Book
from ..models.user import User
from ..extensions import db
from . import collection_bp


@collection_bp.route('/', methods=['POST'])
def create_collection():
    response = {
        'message': 'create collection fail, ',
        'success': False
    }
    try:
        name = request.json.get('name')
        description = request.json.get('description')
        isPublic = request.json.get('isPublic')
        if len(name) == 0:
            raise Exception('collection can not be empty')
        if len(description) > 200:
            raise Exception('Description is too long, should be less than 200 chars')
        user = g.current_user
        collection = Collection(name=name, description=description, isPublic=isPublic)
        collection.users.append(user)
        db.session.add(collection)
        db.session.commit()
        response['success'] = True
        response['message'] = f'create collection {name} success'
        return jsonify(response)
    except Exception as e:
        response['message'] = response['message'] + str(e)
    return jsonify(response)


@collection_bp.route('/', methods=['PUT'])
def edit_collection():
    response = {
        'message': 'edit collection fail, ',
        'success': False
    }
    try:
        name = request.json.get('name')
        description = request.json.get('description')
        collection_id = request.json.get('cid')
        isPublic = request.json.get('isPublic')
        if len(name) == 0:
            raise Exception('collection can not be empty')
        if len(description) > 200:
            raise Exception('Description is too long, should be less than 200 chars')
        c = Collection.query.filter(Collection.id == collection_id).first()
        c.name = name
        c.description = description
        c.isPublic = isPublic
        db.session.commit()
        response['success'] = True
        response['message'] = f'edit collection {name} success'
        return jsonify(response)
    except Exception as e:
        response['message'] = response['message'] + str(e)
    return jsonify(response)

@collection_bp.route('/', methods=['DELETE'])
def delete_collection():
    response = {
        'message': 'delete collection fail, ',
        'success': False
    }
    try:
        collection_id = request.json.get('cid')
        c = Collection.query.filter(Collection.id == collection_id).first()
        db.session.delete(c)
        db.session.commit()
        response['success'] = True
        response['message'] = f'delete collection {c.name} success'
        return jsonify(response)
    except Exception as e:
        response['message'] = response['message'] + str(e)
    return jsonify(response)


@collection_bp.route('/all', methods=['GET'])
def get_collection_list():
    """
    :return: a list of collections which user can join(public)
    """
    response = {
        'collections': [],
        'message': '',
        'success': False
    }
    try:
        collections = Collection.query.filter(Collection.isPublic == True)
        resp = []
        for collection in collections:
            resp.append(collection.to_dict())
        response['collections'] = resp

        joined = []
        uid = g.current_user.id
        readergroups = ReaderGroup.query.filter(ReaderGroup.user_id == uid).all()
        for group in readergroups:
            collection = Collection.query.filter(Collection.id == group.collection_id).first()
            joined.append(collection.to_dict())
        response['joined'] = joined
        response['success'] = True
        return jsonify(response)
    except Exception as e:
        response['message'] = str(e)
    return jsonify(response)


@collection_bp.route('/add_book', methods=['POST'])
def add_book_into_collection():
    response = {
        'message': 'add book into collection fail, ',
        'success': False
    }
    try:
        book_id = request.json.get('bid')
        collection_id = request.json.get('cid')

        collection = Collection.query.filter(Collection.id == collection_id).first()
        book = Book.query.filter(Book.id == book_id).first()

        link = Book_Collection(book_id=book_id, collection_id=collection_id, create_at=int(datetime.now().timestamp()))
        link.book = book
        collection.books.append(link)
        db.session.add(link)
        db.session.commit()

        response['message'] = 'add book into collection successful'
        response['success'] = True

    except Exception as e:
        response['message'] = response['message'] + str(e)
    return jsonify(response)

@collection_bp.route('/delete_book', methods=['DELETE'])
def del_book_from_collection():
    response = {
        'message': 'del book from collection fail, ',
        'success': False
    }
    try:
        book_id = request.json.get('bid')
        collection_id = request.json.get('cid')
        link = Book_Collection.query.filter(Book_Collection.book_id == book_id, Book_Collection.collection_id == collection_id).first()
        db.session.delete(link)
        db.session.commit()
        response['success'] = True
        response['message'] = ''
    except Exception as e:
        response['message'] = response['message'] + str(e)
    return jsonify(response)


@collection_bp.route('/<int:collection_id>', methods=['GET'])
def get_collection_book_list(collection_id):
    response = {
        'books': [],
        'collection': {},
        'success': False,
        'message': 'get collection fail'
    }
    try:
        # # get collection data
        collection = Collection.query.filter(Collection.id == collection_id).first()
        if not collection.isPublic:
            # TODO: check user joined collection or own this collection
            pass
            # abort(404)

        # get book data from associated objects
        links = collection.books
        book_list = []
        for link in links:
            book_list.append(link.book.to_dict())
        response['books'] = book_list
        response['collection'] = collection.to_dict()

        # include list of joined users
        joined = ReaderGroup.query.filter(ReaderGroup.collection_id == collection_id).all()
        users = []
        for user in joined:
            users.append(User.query.filter(User.id == user.user_id).first().to_dict())
        response['collection']['joined'] = users

        response['success'] = True
        response['message'] = 'get collection success'
    except Exception as e:
        response['message'] = response['message'] + str(e)
    return jsonify(response)


@collection_bp.route('/reader/<int:collection_id>', methods=['POST'])
def join_group(collection_id):
    response = {
            'success': False,
            'message': 'join group fail'
            }
    try:
        user = g.current_user

        relation = ReaderGroup(user_id=user.id, collection_id=collection_id)
        db.session.add(relation)
        db.session.commit()
        response['success'] = True
        response['message'] = f'join group success'
        return jsonify(response)
    except Exception as e:
        response['message'] = response['message'] + str(e)
    return jsonify(response)

@collection_bp.route('/reader/<int:collection_id>', methods=['DELETE'])
def leave_group(collection_id):
    response = {
            'success': False,
            'message': 'leave group fail'
            }
    try:
        user = g.current_user

        relation = ReaderGroup.query.filter(ReaderGroup.user_id == user.id, ReaderGroup.collection_id == collection_id).first()
        db.session.delete(relation)
        db.session.commit()
        response['success'] = True
        response['message'] = f'leave group success'
        return jsonify(response)
    except Exception as e:
        response['message'] = response['message'] + str(e)
    return jsonify(response)
