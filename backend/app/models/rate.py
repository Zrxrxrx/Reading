from ..extensions import db
from .book import Book
from .user import User


class Rate(db.Model):
    __tablename__ = 'rate'
    rate = db.Column(db.Integer, unique=False, nullable=False)
    book = db.Column(db.Integer, db.ForeignKey('book.id'), index=True, nullable=False, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), index=True, nullable=False, primary_key=True)
