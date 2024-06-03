from ..extensions import db
from datetime import datetime

class User_Tag(db.Model):
    __tablename__ = 'user_tag'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), primary_key=True)
    weight = db.Column(db.Integer)
    tag = db.relationship('Tag', back_populates="users")
    user = db.relationship('User', back_populates="tags")

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    age = db.Column(db.Integer)
    registerDate = db.Column(db.Integer, nullable=False)
    monthlyGoal = db.Column(db.Integer, default=10)
    avatar = db.Column(db.String(64))
    isAdmin = db.Column(db.Boolean, default=False)
    qualityUser = db.Column(db.Boolean, default=False)
    nameColor = db.Column(db.String(32))
    aboutMe = db.Column(db.String(500))
    read_collection_id = db.Column(db.Integer)


    incorrectTry = db.Column(db.Integer, default=0, nullable=False)
    blocked = db.Column(db.Boolean, default=False, nullable=False)

    tags = db.relationship("User_Tag", back_populates="user")

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        return {'id': self.id, 'username': self.username, 'nameColor': self.nameColor, 'avatar': self.avatar}


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, unique = True, primary_key = True)
    name = db.Column(db.String(20), unique = True)

    books = db.relationship('Book_Tag', back_populates="tag")
    users = db.relationship('User_Tag', back_populates="tag")

    def __repr__(self):
        return f'<Tag {self.id} {self.name}>'





user_book = db.Table('user_book',
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('book_id', db.Integer, db.ForeignKey('book.id')))
