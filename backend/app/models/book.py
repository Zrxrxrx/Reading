from ..extensions import db


class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    author = db.Column(db.String(50), unique=False, nullable=False)
    edition = db.Column(db.String(80), unique=False, nullable=False)
    isbn = db.Column(db.String(13), unique=False, nullable=False)
    categories = db.Column(db.String(130), unique=False, nullable=False)
    introduce = db.Column(db.String(130), unique=False, nullable=False)
    dop = db.Column(db.String(20), unique=False, nullable=False)
    purchase = db.Column(db.String(130), unique=False)
    cover = db.Column(db.String(130), unique=False)
    read_counter = db.Column(db.Integer, nullable=False, default=0)

    collections = db.relationship("Book_Collection", back_populates="book")
    tags = db.relationship("Book_Tag", back_populates="book")

    def __repr__(self):
        return f'<Book {self.name}>'

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'author': self.author,
                'edition': self.edition, 'isbn': self.isbn, 'categories': self.categories,
                'introduce': self.introduce, 'purchase': self.purchase,
                'dop': self.dop, 'cover': self.cover, 'read_counter': self.read_counter}


class Book_Tag(db.Model):
    __tablename__ = 'book_tag'
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), primary_key=True)
    weight = db.Column(db.Integer)
    tag = db.relationship('Tag', back_populates="books")
    book = db.relationship('Book', back_populates="tags")