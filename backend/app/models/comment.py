from ..extensions import db
from datetime import datetime

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    content = db.Column(db.String(1000))
    created_at = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    username = db.Column(db.String(255), nullable=False)
    collection_id = db.Column(db.Integer, db.ForeignKey('collection.id'))

    def __repr__(self):
        return f'<Comment {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'created_at': self.created_at,
            'user_id': self.user_id,
            'username': self.username,
            'collection_id': self.collection_id
        }
