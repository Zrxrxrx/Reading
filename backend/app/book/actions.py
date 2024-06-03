from flask import request, jsonify
from . import bookapi
from ..models.book import Book
from ..models.rate import Rate
from ..models.user import *
from ..extensions import db
from sqlalchemy.sql import func
from sqlalchemy import and_, or_, not_

# create book
@bookapi.route('/create_book', methods=['POST'])
def new_book():
    response = {
        'message': 'application/json is not start with application/json',
        'success': False
    }

    # limit requests content type starts with 'application/json'
    if request.content_type.startswith('application/json'):
        # set params
        name = request.json.get('name')
        author = request.json.get('author')
        edition = request.json.get('edition')
        isbn = request.json.get('isbn')
        categories = request.json.get('categories')
        purchase = request.json.get('purchase')
        introduce = request.json.get('introduce')
        cover = request.json.get('cover')
        # create book
        book = Book(name=name, author=author, edition=edition, isbn=isbn, categories=categories,
                    introduce=introduce, purchase=purchase, cover=cover)
        db.session.add(book)
        db.session.commit()
        response['success'] = True
        response['message'] = 'create book successful!'
        return jsonify(response)

    return jsonify(response)


@bookapi.route('/modify_book', methods=['PUT'])
def modify_book():
    response = {
        'message': 'modify book data fail',
        'success': False
    }
    try:
        # set params
        _id = request.json.get('id')
        name = request.json.get('name')
        author = request.json.get('author')
        edition = request.json.get('edition')
        isbn = request.json.get('isbn')
        categories = request.json.get('categories')
        purchase = request.json.get('purchase')
        introduce = request.json.get('introduce')
        cover = request.json.get('cover')
        # update message
        book = Book.query.filter(Book.id == _id).first()
        book.name = name
        book.author = author
        book.edition = edition
        book.isbn = isbn
        book.categories = categories
        book.purchase = purchase
        book.introduce = introduce
        book.cover = cover
        db.session.commit()
        response['success'] = True
        response['message'] = f'update {name} successful'
    except:
        pass
    return jsonify(response)

# list all book with rating
@bookapi.route('/bookList', methods=['GET'])
def bookList():
    # todo :support search
    response = {
        'books': [],
        'success': False
    }
    books = Book.query.all()
    books_list = []
    # generate average ratings
    raw_ratings = Rate.query.all()
    ratings = raw_ratings
    for book in books:
        book_obj = book.to_dict()
        print(book_obj)
        book_ratings = [a.rate for a in ratings if a.book == book_obj["id"]]
        if len(book_ratings) != 0:
            avg = sum(book_ratings)/len(book_ratings)
        else:
            avg = 0
        book_obj["avg_rating"] = avg
        book_obj["ratings"] = book_ratings
        response['books'].append(book_obj)
    response['success'] = True
    return jsonify(response)

# query book
@bookapi.route('/search', methods=['POST'])
def search():
    response = {
        'message': 'application/json is not start with application/json',
        'success': False
    }

    query = f"%{request.json.get('query')}%"
    if query == None:
        response['message'] = 'Received invalid query'
        return response

    # limit requests content type starts with 'application/json'
    if request.content_type.startswith('application/json'):
        books1 = Book.query.filter(
                    or_(
                        Book.isbn.like(query),
                        Book.name.like(query)
                        )
                    )
        books2 = Book.query.filter(
                    or_(
                        Book.author.like(query),
                        Book.edition.like(query)
                    )
                )
        books = books1.union(books2).all()

        response['books'] = []
        # generate average ratings
        raw_ratings = Rate.query.all()
        ratings = raw_ratings
        for book in books:
            book_obj = book.to_dict()
            print(book_obj)
            book_ratings = [a.rate for a in ratings if a.book == book_obj["id"]]
            if len(book_ratings) != 0:
                avg = sum(book_ratings)/len(book_ratings)
            else:
                avg = 0
            book_obj["avg_rating"] = avg
            book_obj["ratings"] = book_ratings
            response['books'].append(book_obj)
        # TODO: Fallback on the categories, then on the introduction text contents
        response['success'] = True
        response['message'] = 'Search successful'
        return jsonify(response)

    return jsonify(response)

# delete book
@bookapi.route('/delete/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    response = {
        'message': 'delete fail',
        'success': False
    }
    # todo: return book rate from Rate model（avg.）
    try:
        book = Book.query.filter(Book.id == book_id).first()
        links = Book_Tag.query.filter(Book_Tag.book_id == book_id).all()
        db.session.delete(links)
        db.session.delete(book)
        db.session.commit()
        response['success'] = True
        response['message'] = f'delete {book.name} successful'
    except:
        # todo：save logging
        pass
    return jsonify(response)

# get book infomaion by book id
@bookapi.route('/<int:book_id>', methods=['GET'])
def book_info(book_id):
    response = {
        'message': '',
        'success': False
    }

    try:
        book = Book.query.filter(Book.id == book_id).first()
        response['book'] = book.to_dict()
        response['success'] = True
    except Exception as e:
        response['message'] = str(e)
    return jsonify(response)


@bookapi.route('/rank', methods=['post'])
def book_rank():
    """
    inner join rate and book,
    and then group the scoring table according to the book ID to find the average ranking
    for example:
    select b.id,name,author,edition,isbn,categories,introduce,avg(rate) as rate
    from rate inner join book b on b.id = rate.book
    where categories like '%dwah%'
    group by b.id
    order by rate desc
    limit 20
    :param: category<string>,page<int>
    :return:book rank list
    """
    response = {
        'message': '',
        'result': [],
        'success': False
    }
    # default page is 20,category no limit
    try:
        page_num = request.json.get('page')
        category = request.json.get('category')
        if not page_num:
            page_num = 20
        if category:
            sql = f"""select b.id,name,author,edition,isbn,categories,introduce,cover,avg(rate) as rate
            from rate inner join book b on b.id = rate.book
            where categories like '%{category}%'
            group by b.id
            order by rate desc
            limit {page_num}"""
        else:
            sql = f"""select b.id,name,author,edition,isbn,categories,introduce,cover,avg(rate) as rate
                    from rate inner join book b on b.id = rate.book
                    group by b.id
                    order by rate desc
                    limit {page_num}"""
        rows = db.session.execute(sql)
        resp = []
        for x in rows.fetchall():
            resp.append(
                {"book_id": x[0], "book_name": x[1], "author": x[2], "edition": x[3], "isbn": x[4], "categories": x[5],
                 "introduce": x[6], "cover": x[7], "rate": round(x[8], 2)})
        response['result'] = resp
        response['success'] = True
        response['message'] = "find book ranking ok"
    except Exception as e:
        response['message'] = response['message'] + str(e)
    return jsonify(response)
