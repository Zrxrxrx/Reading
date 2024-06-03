from ..extensions import db
from ..models.user import User
from ..models.book import Book
from ..models.rate import Rate


class Review(db.Model):
    __tablename__ = 'review'
    __table_args__ = {'extend_existing': False}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    # min 100 max 1000 words
    content = db.Column(db.String(5000), nullable=False, unique=False)
    create_at = db.Column(db.Integer, nullable=False)
    __table_args__ = (db.UniqueConstraint('book_id', 'user_id', name='_book_user_uc'),)

    def to_dict(self):
        rating = 0
        r = Rate.query.filter_by(book=self.book_id, user=self.user_id).first()
        if r:
            rating = r.rate
        return {'id': self.id,
                'book': Book.query.filter(Book.id == self.book_id).first().to_dict(),
                'user': User.query.filter(User.id == self.user_id).first().to_dict(),
                'content': self.content,
                'created_at': self.create_at,
                'rating': rating
                }
