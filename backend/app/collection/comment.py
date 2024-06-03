from flask import request, jsonify, g, abort
from datetime import datetime
from ..models.comment import Comment
from ..models.user import User
from ..extensions import db
from . import collection_bp


@collection_bp.route('/comment/', methods=['GET'])
def get_comments():
    response = {
        'success': False,
        'message': '',
        'comments': []
    }
    try:
        cid = request.args.get('cid')

        if cid is None:
            raise Exception('Collection id is required')
        comments = Comment.query.filter_by(collection_id=cid).all()
        response['success'] = True
        response['message'] = 'Comments fetched successfully'
        comments_list = []
        for comment in comments:
            comment_obj = comment.to_dict()
            comment_obj['user'] = User.query.filter(User.id == comment.user_id).first().to_dict()
            comments_list.append(comment_obj)
        response['comments'] = comments_list
    except Exception as e:
        response['message'] = str(e)

    return jsonify(response)

@collection_bp.route('/comment/', methods=['POST'])
def create_comment():
    response = {
        'success': False,
        'message': '',
        'comment': None
    }
    try:
        user = g.current_user
        data = request.get_json()
        cid = data['cid']

        comment = Comment(user_id=user.id, username=user.username, content=data['content'], collection_id=cid, created_at=datetime.now().timestamp())

        db.session.add(comment)
        db.session.commit()
        db.session.flush()

        response['success'] = True
        response['message'] = 'Comment created successfully'
        response['comment'] = comment.to_dict()
    except Exception as e:
        response['message'] = str(e)

    return jsonify(response)


@collection_bp.route('/comment/<int:id>', methods=['PUT'])
def update_comment():
    pass

@collection_bp.route('/comment/<int:cid>', methods=['DELETE'])
def delete_comment(cid):
    response = {
            'success': False,
            'message': "Failed to remove comment"
            }
    try:
        user = g.current_user

        comment = Comment.query.filter(Comment.id == cid).first()
        if comment.user_id == user.id or user.isAdmin == True:
            db.session.delete(comment)
            db.session.commit()
            response['success'] = True
            response['message'] = "Succesfully removed comment"
        else:
            response['message'] = "You do not have permission to delete that comment"
    except Exception as e:
        response['message'] = str(e)
        print(e)
    return jsonify(response)
