from flask import g, jsonify
from . import user_bp
from ..models.collection import Collection, ReaderGroup


@user_bp.route('/collections', methods=['GET'])
def get_user_collections():
    """
    :return: current user collection list
    """
    response = {
        'collections': [],
        'success': False
    }
    try:
        user = g.current_user
        collections = user.collections
        resp = []
        for collection in collections:
            temp = collection.to_dict()
            temp['books'] = []
            for link in collection.books:
                temp['books'].append(link.book.to_dict())
            resp.append(temp)
        response['collections'] = resp

        joined = []
        uid = g.current_user.id
        readergroups = ReaderGroup.query.filter(ReaderGroup.user_id == uid).all()
        for group in readergroups:
            collection = Collection.query.filter(Collection.id == group.collection_id).first()
            collection_obj = collection.to_dict()
            collection_obj['books'] = []
            for link in collection.books:
                collection_obj['books'].append(link.book.to_dict())
            joined.append(collection_obj)
        response['joined'] = joined
        response['success'] = True
        return jsonify(response)
    except Exception as e:
        response['message'] = str(e)
    return jsonify(response)
