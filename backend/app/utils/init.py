from ..models.user import User
from ..models.book import Book
from ..models.collection import Collection
from ..extensions import db
from datetime import datetime
import sqlalchemy


def init_data():
    success = init_admin()
    if success:
        init_books()



def init_admin():
    admin = User(username='admin', password='iamadmin', email='admin@admin.com', isAdmin=True, nameColor="red", registerDate=int(datetime.now().timestamp()))
    try:
        db.session.add(admin)
        db.session.commit()
        main_collection = Collection(name='main', description='Default Collection', deleteable=False)
        haveRead = Collection(name='Have Read', description='The books you have read.', deleteable=False, isRead=True)
        admin.collections.append(main_collection)
        admin.collections.append(haveRead)
        main_collection.users.append(admin)
        haveRead.users.append(admin)
        db.session.add(main_collection, haveRead)
        db.session.flush()
        admin.read_collection_id = haveRead.id
        return True
    except sqlalchemy.exc.IntegrityError as e:
        print(e)
        print("admin exists")
        return False
    

def init_books():
    book1 = Book(name='book1', author='author1', isbn='123456', categories='test', edition='edition1', introduce='test', dop="2020-01")
    book2 = Book(name='book2', author='author2', isbn='123456', categories='test', edition='edition2', introduce='test', dop="2022-02")
    book3 = Book(name='book3', author='author3', isbn='123456', categories='test', edition='edition3', introduce='test', dop="2022-04")

    db.session.add_all([book1, book2, book3])
    db.session.commit()



