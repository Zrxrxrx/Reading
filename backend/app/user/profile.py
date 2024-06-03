
from flask import request, g
from ..extensions import db
from . import user_bp
from datetime import datetime
from ..models.collection import *
from ..models.book import *
from ..models.rate import *
from ..models.user import User, Tag, User_Tag
from ..models.review import Review

@user_bp.route('/profile', methods=['GET'])
def showProfile():
    response = {
        'name': '', 
        'age': '', 
        'aboutMe': '', 
        'registerDate': '', 
        'accountAge': '', 
        'picURL': '',
        'nameColor': '',
        'goal': 0,
        'tag':[],
        'id': None,
        'success': False
    }
    user = g.current_user

    try:
        tag_links = user.tags
        for tl in tag_links:
            response['tag'].append(tl.tag.name)

        response['name'] = user.username
        response['age'] = user.age
        response['aboutMe'] = user.aboutMe
        response['registerDate'] = user.registerDate
        # response['accountAge'] = user.accountAge
        response['goal'] = user.monthlyGoal
        response['picURL'] = user.avatar
        response['nameColor'] = user.nameColor
        response['id'] = user.id
        response['success'] = True
    except Exception as e:
        print(e)
        pass

    return response

@user_bp.route('profile', methods=['PUT'])
def editProfile():
    response = {
        'success': False
    }

    info = request.get_json()
    user = g.current_user

    try:
        age = info['age']
        aboutMe = info['aboutMe']
        monthlyGoal = info['goal']
        avatar = info['picURL']
        # tags = info['tag']


        # user = User.query.filter(User.id == user_id).first()
        # old_tags = user_tag.query.filter(user_tag.user_id == user_id).all()
        # db.session.delete(old_tags)

        # for x in tags:
            # new_tag = user_tag(user_id = user_id, tag_id = x)
            # db.session.add(new_tag)

        # check age
        if age:
            user.age = age

        # check aboutMe
        if aboutMe:
            user.aboutMe = aboutMe

        if monthlyGoal:
            user.monthlyGoal = monthlyGoal

        if avatar:
            user.avatar = avatar
        
        db.session.commit()

        response['success'] = True
    except Exception as e:
        print(e)

    return response

@user_bp.route('/user/get_all_users', methods=['GET'])
def get_all_users():
    response = {
        'users': [], 
        'success': False
    }

    try:
        all_users = User.query.all()

        for x in all_users:
            response['users'].append(x)
        
        response['success'] = True
    except:
        pass

    return response

# TODO: handle dup tags, edit tag, delete tag
# BUG: duplicate should not allowed
@user_bp.route('/tag', methods=['POST'])
def get_user_tag():
    res = {
        'success': False,
    }

    try:
        data = request.get_json()
        user = g.current_user
        
        tagName = data['name']
        tag = Tag.query.filter(Tag.name == tagName).first()
        if not tag:
            tag = Tag(name=tagName)
            db.session.add(tag)
            db.session.flush()
            db.session.commit()

        link = User_Tag(user_id=user.id, tag_id=tag.id)
        db.session.add(link)
        db.session.commit()

        res['success'] = True
    except Exception as e:
        print(e)

    return res


@user_bp.route('/goal_achieved', methods=['GET'])
def goal_achieved():
    res = {
        'goal_achieved': 0,
        'date': 0,
        'goal_target': 0,
        'isFinish': False,
        'success': False
    }
    try:
        user = g.current_user
        read_collection_id = user.read_collection_id
        this_month_read = 0
        current_month = datetime.now().strftime('%m')

        read_collection = Collection.query.filter(Collection.id == read_collection_id).first()

        links = read_collection.books

        for link in links:
            created_time = datetime.fromtimestamp(link.create_at)
            if created_time.strftime('%m') == current_month:
                this_month_read = this_month_read + 1
                last_date = link.create_at
                if this_month_read == user.monthlyGoal:
                    res['isFinish'] = True
                    res['date'] = last_date

        res['goal_achieved'] = this_month_read
        res['goal_target'] = user.monthlyGoal
        res['success'] = True
        
    except Exception as e:
        print(e)

    return res


@user_bp.route('/nameColor', methods=['GET'])
def getNameColors():
    response = {
        'colors': []
    }

    info = request.get_json()
    user = g.current_user
    colors = ["black (Default)"]

    # red color is exclusive for admins
    if user.isAdmin == True:
        colors.append("red (Exclusive for Administrators)")

    joined = ReaderGroup.query.filter(ReaderGroup.user_id == user.id).all()
    if len(joined) != 0:
        colors.append("green (Joined a Reader Group)")

    try:
        read_collection_id = user.read_collection_id
        this_month_read = 0
        current_month = datetime.now().strftime('%m')

        read_collection = Collection.query.filter(Collection.id == read_collection_id).first()

        links = read_collection.books

        for link in links:
            created_time = datetime.fromtimestamp(link.create_at)
            if created_time.strftime('%m') == current_month:
                this_month_read = this_month_read + 1
                last_date = link.create_at
                if this_month_read == user.monthlyGoal:
                    res['isFinish'] = True
                    res['date'] = last_date

        if user.monthlyGoal <= this_month_read:
            colors.append("orange (Completed monthly read goal)")
    
    except Exception as e:
        print(e)

    if len(user.collections) > 5:
        colors.append("yellow (More than 5 collections)")

    reviews = Review.query.filter(Review.user_id == user.id).all()
    if len(reviews) > 0:
        colors.append("blue (Leave a review on a book you have read)")

    response['colors'] = colors

    return response


@user_bp.route('/nameColor', methods=['POST'])
def editNameColor():
    response = {
        'success': False
    }

    info = request.get_json()
    user = g.current_user

    try:
        color = info['nameColor']
        user.nameColor = color
        db.session.commit()

        response['success'] = True
    except Exception as e:
        print(e)
    return response
