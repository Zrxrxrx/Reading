from ..extensions import db
from datetime import datetime

class Book_Collection(db.Model):
    __tablename__ = 'book_collection'
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)
    collection_id = db.Column(db.Integer, db.ForeignKey('collection.id'), primary_key=True)
    create_at = db.Column(db.Integer)
    collection = db.relationship('Collection', back_populates="books")
    book = db.relationship('Book', back_populates="collections")

user_collection = db.Table('user_collection',
                           db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                           db.Column('collection_id', db.Integer, db.ForeignKey('collection.id')))


class Collection(db.Model):
    __tablename__ = 'collection'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    description = db.Column(db.String(120), unique=False, nullable=False)
    isPublic = db.Column(db.Boolean, nullable=False, default=False)
    users = db.relationship('User', secondary=user_collection, backref="collections")

    books = db.relationship('Book_Collection', back_populates="collection")

    isRead = db.Column(db.Boolean, nullable=False, default=False)
    deleteable = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return f'<Collection {self.name}>'

    def to_dict(self):
        return {'id': self.id,
                'name': self.name,
                'description': self.description,
                'isPublic': self.isPublic,
                'isRead': self.isRead,
                'deleteable': self.deleteable,
                'owner': self.users[0].to_dict()
                }

class ReaderGroup(db.Model):
    __tablename__ = 'reader_group'
    relation_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    collection_id = db.Column(db.Integer, db.ForeignKey('collection.id'), nullable=False)

