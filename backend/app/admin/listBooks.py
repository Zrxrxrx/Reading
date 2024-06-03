from flask import request
from ..extensions import db
from . import admin_bp
from ..models.book import Book

# fetch all books from the database
@admin_bp.route('listBooks', methods=['GET'])
def listBooks():
    response = {
        'books': '', 
        'success': False
    }

    data = [{ "id": book.id, "name": book.name, "author": book.author, "edition": book.edition, "categories": book.categories } for book in Book.query.all()]
    response['success'] = True
    response['books'] = data

    return response