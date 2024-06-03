from flask import jsonify, g
from . import bookapi
from ..models.book import Book
from ..models.rate import Rate
from ..models.collection import Collection

"""
user_recommend api can get all appear times of tags in read collection, and find
all times of tags in all books. also, the books author will be count on a element,
it will return a descending order book list with its rates.
"""
@bookapi.route('/recommend', methods=['GET'])
def recommend():
    res = {
        'books': [],
        'success': False
    }

    try:
        user = g.current_user
        all_books = Book.query.all()
        all_books_score = [Book_score(book=book, score=0) for book in all_books]

        read_collection = Collection.query.filter(Collection.id == user.read_collection_id).first()
        links = read_collection.books
        read_books = [link.book for link in links]

        candidateBooks = __remove_read_book(all_books_score, read_books)

        read_author = __read_authors(read_books)  # store all read books' authors
        __evaluate_books_by_author(candidateBooks, read_author, weight=1)

        user_tags = __user_tags(user)
        __evaluate_books_by_user_tags(candidateBooks, user_tags, weight=1)

        read_tags = __read_tags(read_books)
        __evaluate_books_by_read_tags(candidateBooks, read_tags, weight=1)

        __evaluate_books_by_rating(candidateBooks, weight=1)


        res['books'] = [bs.get_book() for bs in sorted(candidateBooks, key=lambda bs: bs.score, reverse=True)]
        res['success'] = True

    except Exception as e:
        print(e)
        res['message'] = str(e)

    print(candidateBooks)
    return jsonify(res)


def __read_authors(read_books):
    author_dict = {}
    for book in read_books:
        author = book.author
        if author_dict.get(author) is None:
            author_dict[author] = 1
        else:
            author_dict[author] += 1
    return author_dict


def __evaluate_books_by_author(all_books_score, author_dict, weight=1):
    for bs in all_books_score:
        bs.total += len(author_dict) * weight
        if bs.book.author in author_dict:
            bs.score += author_dict[bs.book.author] * weight


def __user_tags(user):
    return [link.tag for link in user.tags]


def __evaluate_books_by_user_tags(candidateBooks, user_tags, weight=1):
    for bs in candidateBooks:
        bs.total += len(user_tags) * weight
        links = bs.book.tags
        book_tags = [link.tag for link in links]
        for tag in book_tags:
            if tag in user_tags:
                bs.score += 1 * weight


def __evaluate_books_by_read_tags(candidateBooks, read_tags, weight=1):
    for bs in candidateBooks:
        bs.total += len(read_tags) * weight
        links = bs.book.tags
        book_tags = [link.tag for link in links]
        for tag in book_tags:
            if tag in read_tags:
                bs.score += read_tags[tag] * weight


def __read_tags(read_books):
    tag_dict = {}
    for book in read_books:
        tags = [link.tag for link in book.tags]
        for tag in tags:
            if tag_dict.get(tag) is None:
                tag_dict[tag] = 1
            else:
                tag_dict[tag] += 1

    return tag_dict


def __evaluate_books_by_rating(candidateBooks, weight=1):
    for bs in candidateBooks:
        bs.total += 5 * weight
        ratings = Rate.query.filter_by(book=bs.book.id).all()
        if len(ratings) == 0:
            continue
        sum = 0
        for rating in ratings:
            sum += rating.rate
        ave = sum / len(ratings)
        bs.score += ave * weight


def __remove_read_book(all_books_score, read_books):
    result = []
    for bs in all_books_score:
        if bs.book in read_books:
            pass
        else:
            result.append(bs)

    return result


class Book_score():
    def __init__(self, book, score=0):
        self.book = book
        self.score = score
        self.total = 0

    def get_book(self):
        book_dict = self.book.to_dict()
        book_dict['percentage'] = max((self.score / self.total) * 100, 10)
        return book_dict

    def __repr__(self):
        return f'<Book_score {self.book.name} {self.score}>'
