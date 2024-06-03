from flask import request, jsonify, g
from ..models.rate import Rate
from ..extensions import db
from . import rate_bp
import sqlalchemy



@rate_bp.route('/', methods=['POST'])
def rating():
    """
    :example:
    curl --location --request POST '127.0.0.1:5000/rate/rating' \
    --header 'Content-Type: application/json' \
   --data-raw '{"bid":1,"rate":5}'
    :return:
    """
    response = {
        'message': 'Rating fail, ',
        'success': False
    }
    try:
        bid = request.json.get('bid')  # book_id
        rate = request.json.get('rating')  # rate
        if rate > 5:
            raise "the rate must be less than 5"
        user = g.current_user
        # for test
        # r = Rate(rate=rate, book=bid, user=1)
        r = Rate(rate=rate, book=bid, user=user.id)
        db.session.add(r)
        db.session.commit()
        response['success'] = True
        response['message'] = f'Rating book id: {bid} success'
        return jsonify(response)
    except sqlalchemy.exc.IntegrityError:
        response['message'] = response['message'] + 'You have rated this book'
    except Exception as e:
        response['message'] = response['message'] + str(e)
    return jsonify(response)

@rate_bp.route('/<int:bid>', methods=['GET'])
def get_avg_rating(bid):
    response = {
        'message': 'get rating fail, ',
        'success': False,
        'avg_rating': 0
    }
    try:
        rates = Rate.query.filter_by(book=bid).all()
        if rates:
            total = 0
            for rate in rates:
                total += rate.rate
            avg = total / len(rates)
            response['avg_rating'] = avg
        else:
            response['avg_rating'] = 0
        response['success'] = True
        response['message'] = f'get rating book id: {bid} success'
        return jsonify(response)
    except Exception as e:
        response['message'] = response['message'] + str(e)
    return jsonify(response)
