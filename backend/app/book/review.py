from flask import request, jsonify, g
from app.models.review import Review
from app.models.user import User
from app.models.rate import Rate
from app.extensions import db
from ..book import bookapi
from datetime import datetime
import sqlalchemy


# create review for book by book id,
# each user can only create one review for one book
@bookapi.route('/review/', methods=['POST'])
def add_review():
    """
    create review
    :return:
    """
    response = {
        'message': 'create review fail, ',
        'success': False,
        'review': None
    }
    try:
        bid = request.json.get('bid')  # book_id
        content = request.json.get('content')  # content
        if len(content.split(' ')) < 100:
            raise Exception("the review words must be more than 100.")
        if len(content.split(' ')) > 1000:
            raise Exception("the review words must be less than 1000.")
        user = g.current_user

        rating = Rate.query.filter(Rate.user == user.id, Rate.book == bid).first()
        if not rating:
            raise Exception("The book is not rated, you should mark it read first.")

        r = Review(book_id=bid, user_id=user.id, content=content, create_at=int(datetime.now().timestamp()))
        db.session.add(r)
        db.session.commit()
        db.session.flush()
        response['success'] = True
        response['message'] = f'review book id: {bid} success'
        response['review'] = r.to_dict()
    except sqlalchemy.exc.IntegrityError as e:
        response['message'] = response['message'] + "review already exist."
    except Exception as e:
        response['message'] = response['message'] + str(e)
    return jsonify(response)

# modify review by review id
@bookapi.route('/review/', methods=['PUT'])
def update_review():
    """
    edit review
    :return:
    """
    response = {
        'message': 'edit review fail, ',
        'success': False,
        'review': None
    }
    try:
        rid = request.json.get('rid')  # review_id
        bid = request.json.get('bid')  # book_id
        content = request.json.get('content')  # content
        if len(content.split(' ')) < 100:
            raise Exception("the review words must be more than 100.")
        if len(content.split(' ')) > 1000:
            raise Exception("the review words must be less than 1000.")
        user = g.current_user

        rating = Rate.query.filter(Rate.user == user.id, Rate.book == bid).first()
        if not rating:
            raise Exception("The book is not rated, you should mark it read first.")

        r = Review.query.filter(Review.book_id == bid, Review.user_id == user.id).first()
        r.content = content
        db.session.commit()
        response['success'] = True
        response['message'] = f'edit review book id: {bid} success'
        response['review'] = r.to_dict()
    except Exception as e:
        response['message'] = response['message'] + str(e)
    return jsonify(response)

# delete review by review id
@bookapi.route('/review/<int:rid>', methods=['DELETE'])
def delete_review(rid):
    response = {
            'success': False,
            'message': "Failed to remove review"
            }
    try:
        user = g.current_user

        review = Review.query.filter(Review.id == rid).first()
        if review.user_id == user.id or user.isAdmin == True:
            db.session.delete(review)
            db.session.commit()
            response['success'] = True
            response['message'] = "Succesfully removed review"
        else:
            response['message'] = "You do not have permission to delete that review"
    except Exception as e:
        response['message'] = str(e)
        print(e)
    return jsonify(response)

# todo: return review list of book
@bookapi.route('/review/', methods=['GET'])
def review_list():
    """

    :return:
    """
    response = {
        'message': 'get review list fail, ',
        'success': False
    }
    try:
        bid = request.args.get('bid')  # book_id
        # page = request.json.get('page')
        # page_size = request.json.get('page_size')
        # reviews = Review.query.filter(Review.book_id == bid).order_by(Review.create_at.desc()).paginate(page,
        # page_size, False)
        reviews = Review.query.filter(Review.book_id == bid).order_by(Review.create_at.desc()).all()
        preview = []
        for review in reviews:
            review_obj = review.to_dict()
            review_obj['user'] = User.query.filter(review.user_id == User.id).first().to_dict()
            preview.append(review_obj)
        response['success'] = True
        response['reviews'] = preview
        response['message'] = f'review book id: {bid} success'
        return jsonify(response)
    except Exception as e:
        response['message'] = response['message'] + str(e)
    return jsonify(response)
